#!/usr/bin/env python3
"""Deterministic validation for the Iridlab bubble membrane specimen."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN = ROOT / "specimens" / "bubble_membrane"
MAPS = SPECIMEN / "maps"
MANIFEST_PATH = SPECIMEN / "manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image(name: str) -> np.ndarray:
    return np.array(Image.open(SPECIMEN / name))


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS {message}")


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text())
    check(manifest["specimen"] == "bubble_membrane", "manifest identifies bubble_membrane")

    for rel, expected in manifest["files"].items():
        path = SPECIMEN / rel
        check(path.is_file(), f"file exists: {rel}")
        check(sha256(path) == expected["sha256"], f"sha256 matches: {rel}")
        if rel.endswith(".png"):
            with Image.open(path) as img:
                check(list(img.size) == expected["size"], f"dimensions match: {rel}")

    ao = image("maps/ambient_occlusion.png")
    roughness = image("maps/roughness.png")
    metalness = image("maps/metalness.png")
    orm = image("maps/orm.png")
    check(np.array_equal(orm[:, :, 0], ao), "ORM R equals ambient occlusion")
    check(np.array_equal(orm[:, :, 1], roughness), "ORM G equals roughness")
    check(np.array_equal(orm[:, :, 2], metalness), "ORM B equals metalness")

    mask = image("maps/iridescence_mask.png")
    thickness = image("maps/iridescence_thickness_normalized.png")
    packed = image("maps/iridescence_packed_rg.png")
    thickness_8 = np.rint(thickness / 257.0).astype(np.uint8)
    check(np.array_equal(packed[:, :, 0], mask), "packed iridescence R equals mask")
    check(np.array_equal(packed[:, :, 1], thickness_8), "packed iridescence G equals quantized thickness")
    check(np.all(packed[:, :, 2] == 0), "packed iridescence B is unused/zero")

    reference_mask = image("reference_mask.png")
    reference = image("reference_crop.png")
    check(np.array_equal(reference[:, :, 3] > 0, reference_mask > 0), "reference alpha coverage equals mask coverage")
    check(np.unique(image("maps/height.png")).size == 1, "height map is constant as documented")
    check(np.unique(image("maps/normal.png").reshape(-1, 3), axis=0).tolist() == [[128, 128, 255]], "normal map is flat OpenGL tangent normal")

    print("PASS specimen validation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
