# Reproduce the Bubble Membrane Runtime

## Clone

```bash
git clone https://github.com/qt314wink/pompa-iridiscencia.git
cd pompa-iridiscencia
git switch feat/iridlab-bubble-membrane-runtime
```

The branch is intentionally a reviewable feature branch. The default `main` branch remains the prior simulator state until the pull request is reviewed.

## Validate specimen packaging

<!-- coderabbit-ai-generated:v1 -->

<!-- coderabbit-ai-generated-section:v1:11577cbc20c585de49f110ec8bb9a010854f9312206fc81bab49f08b53b0daed -->

The validator uses Python 3.11 or newer with the pinned NumPy and Pillow versions in `requirements-dev.txt`:

<!-- /coderabbit-ai-generated:v1 -->

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python3 tests/validate_specimen.py
```

Expected result: a zero exit code with `PASS` lines for manifest hashes, dimensions, ORM packing, iridescence packing, and reference alpha/mask parity.

## Start the browser runtime

No Node build is required for the existing browser simulator or evidence viewer. Serve the repository so ES modules and local specimen assets load correctly:

```bash
python3 -m http.server 4173 --directory .
```

Open:

- Simulator: <http://127.0.0.1:4173/docs/index.html>
- Specimen evidence viewer: <http://127.0.0.1:4173/docs/specimen.html>

Do not open the HTML with `file://`; browser module and asset policies can make that path misleading.

## What to look for

1. The simulator should load a visible bubble and expose camera, light, IOR, thickness, and transmission controls.
2. The evidence viewer should show the supplied reference crop, CPU diagnostic, and map channels without rewriting source assets.
3. Use the ledger and validation plan to distinguish a visual resemblance from a controlled render claim.
4. Record browser, GPU, viewport, fixture ID, and source hashes for any new screenshot.

## Available test package

<!-- coderabbit-ai-generated:v1 -->

<!-- coderabbit-ai-generated-section:v1:026fd4219a494835d94c69590de6416a8c98f826cecd0b919f39414bdc4453d5 -->

The repository pins NumPy and Pillow in `requirements-dev.txt`. The validator is deterministic and does not need API keys, a database, or a proprietary service. It also checks that the copies published under `docs/specimens/` match the source manifest; update those copies whenever the source specimen changes. The browser runtime uses the existing CDN imports declared in `docs/index.html`.

<!-- /coderabbit-ai-generated:v1 -->

## Research and decision records

- `docs/BUBBLE_MEMBRANE_EXPERIMENT_LEDGER.md` — authority, evidence classes, gates, lineage, rollback.
- `docs/BUBBLE_MEMBRANE_VALIDATION_PLAN.md` — positive, negative, null, seam, and mobile fixtures.
- `docs/BUBBLE_MEMBRANE_DECISION_LOG.md` — dated decisions and rejected alternatives.
- `specimens/bubble_membrane/material.json` — source material declaration.
- `specimens/bubble_membrane/manifest.json` — hashes, dimensions, and measured map relationships.
