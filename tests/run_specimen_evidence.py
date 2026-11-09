"""Run the bubble specimen validator and record static serving evidence."""

import argparse
from datetime import datetime, timezone
import hashlib
from http.client import HTTPException
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from importlib.metadata import version
import json
import os
from pathlib import Path
import subprocess
import sys
from threading import Thread
from time import monotonic
from urllib.error import URLError
from urllib.request import build_opener, ProxyHandler

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MANIFEST = ROOT / "specimens/bubble_membrane/manifest.json"
SERVED_PATHS = (
    "index.html", "specimen.html", "app.js", "shader.js",
    "specimens/bubble_membrane/manifest.json",
    "specimens/bubble_membrane/material.json",
    "specimens/bubble_membrane/maps/iridescence_packed_rg.png",
)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class StaticFiles(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOCS, **kwargs)

    def log_message(self, *args):
        pass


def probe_routes(revision):
    opener = build_opener(ProxyHandler({}))
    results = []
    with ThreadingHTTPServer(("127.0.0.1", 0), StaticFiles) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for path in SERVED_PATHS:
                started = monotonic()
                row = {"path": "/" + path}
                try:
                    expected = subprocess.check_output(
                        ["git", "show", f"{revision}:docs/{path}"], cwd=ROOT,
                        stderr=subprocess.DEVNULL,
                    )
                    row["expected_sha256"] = sha256(expected)
                    url = f"http://127.0.0.1:{server.server_port}/{path}"
                    with opener.open(url, timeout=5) as response:
                        actual = response.read(len(expected) + 1)
                        row.update(status=response.status, sha256=sha256(actual), bytes=len(actual))
                        row["pass"] = response.status == 200 and actual == expected
                except subprocess.CalledProcessError:
                    row.update({"pass": False, "error": "Required Git blob is missing"})
                except (URLError, OSError, HTTPException) as error:
                    row.update({"pass": False, "error": str(error)})
                row["elapsed_ms"] = round((monotonic() - started) * 1000, 1)
                results.append(row)
        finally:
            server.shutdown()
            thread.join()
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="new JSON receipt path")
    args = parser.parse_args()
    if args.out.exists():
        parser.error("--out must be a new file")
    head = git("rev-parse", "HEAD")
    dirty = bool(git("status", "--porcelain", "--untracked-files=normal"))
    command = [sys.executable, "tests/validate_specimen.py"]
    started = monotonic()
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    validator = {
        "command": ["python3", "tests/validate_specimen.py"],
        "exit_code": process.returncode,
        "elapsed_ms": round((monotonic() - started) * 1000, 1),
        "assertions_passed": sum(line.startswith("PASS ") for line in process.stdout.splitlines()),
        "stdout": process.stdout,
        "stderr": process.stderr,
    }
    routes = probe_routes(head) if process.returncode == 0 else []
    passed = process.returncode == 0 and len(routes) == len(SERVED_PATHS) and all(
        row["pass"] for row in routes
    )
    receipt = {
        "schema_version": 1,
        "workflow": "bubble-membrane-g0",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "revision": head,
        "checkout_dirty_before_measurement": dirty,
        "python": sys.version.split()[0],
        "numpy": version("numpy"),
        "pillow": version("Pillow"),
        "ci_run": os.getenv("GITHUB_RUN_ID"),
        "specimen_manifest_sha256": sha256(MANIFEST.read_bytes()) if MANIFEST.exists() else None,
        "validator": validator,
        "routes": routes,
        "result": "pass" if passed else "fail",
        "scope": "Specimen packaging and byte-exact loopback HTTP under docs/",
        "open_gates": ["Target-device GPU", "Deployed routes", "Optical calibration", "Named art direction"],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(f"{receipt['result']}: {validator['assertions_passed']} validator checks, "
          f"{sum(row['pass'] for row in routes)}/{len(SERVED_PATHS)} routes; {args.out}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
