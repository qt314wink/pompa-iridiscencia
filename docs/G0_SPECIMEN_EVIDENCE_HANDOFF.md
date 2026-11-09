# G0 bubble specimen evidence

[PR #1](https://github.com/qt314wink/pompa-iridiscencia/pull/1) contains the specimen, its independent required-file inventory, the simulator, and the validation plan. This workflow runs the existing validator and checks that a loopback server delivers seven committed resources from the publishable `docs/` directory. It emits one JSON receipt with environment, commit, manifest digest, command output, per-route observations and residual gates.

## Run

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tests/run_specimen_evidence.py --out /tmp/bubble-specimen.json
```

Use a fresh output path. The packaging contract requires the existing validator's zero exit and exact manifest, dimensions, channel packing and source/published parity. The serving contract requires seven HTTP 200 responses and byte equality with the corresponding Git blobs. A packaging failure skips the HTTP measurements and preserves the validator output. The receipt includes elapsed times to aid diagnosis. Treat them as descriptive loopback measurements.

## Agent handoff

- **Orient.** Resolve the full PR head and read the [validation plan](BUBBLE_MEMBRANE_VALIDATION_PLAN.md), [G1 contract](G1_RENDERER_BINDING_CONTRACT.md) and [existing renderer receipt](g1_binding_receipt.json). Verify the historical receipt's runtime, shader and fixture identity before using any of its measurements.
- **Verify.** Run the command in a clean checkout. If it fails, keep the JSON and identify the first failed invariant. Reproduce any suspect condition in a disposable checkout. A changed published map must fail before serving checks. Leave original files intact.
- **Draft the next experiment.** After G0 passes, compare the pinned renderer's positive, null and negative control at a fixed camera, lighting and exposure. Ask the reviewer to set an image-error budget for a lower sample count before evaluating mobile performance. For each result record renderer, device, pixel ratio, seed or fixed inputs, capture digest, output statistics, and a reviewer judgment about continuity of the film.
- **Return.** Include repository, full source and tested SHA, commands and exit codes, JSON hash, observed checks, renderer and device residuals, and the next review decision. Stop at scope drift, rights gaps or an unrepeatable baseline. Keep creative edits in a separate draft with origin, asset rights and paired captures. Leave deployment and specimen promotion to the owner.

The Actions receipt is retained for 14 days. Preserve the result and receipt hash with any durable decision. G0 informs a later renderer review and covers packaging and local serving only.
