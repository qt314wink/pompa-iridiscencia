# Iridlab Bubble Membrane — Experiment Ledger

**Status:** `GENERATED_HYPOTHESIS / APPLIED-MATERIAL CANDIDATE`
**Specimen:** `specimens/bubble_membrane/`
**Source package:** `iridlab_bubble_membrane_v0_1.zip`
**Runtime:** `docs/index.html` (WebGL thin-film simulator) and `docs/specimen.html` (evidence viewer)

## Intent

Make the bubble material reproducible and reviewable without promoting a visually plausible result to calibrated physical truth. The supplied maps are synthetic starting values. This branch preserves the source specimen, records its derived relationships, and adds a browser-visible evidence path.

## Authority and lineage

- The source specimen archive is the authority for the supplied maps and `material.json`.
- The existing WebGL simulator is a related executable runtime for thin-film interference, not proof that the supplied maps are currently bound to the renderer.
- The new evidence viewer is a diagnostic/documentation surface. It does not replace the physical simulator or claim renderer equivalence.
- No source pixels, numeric material values, or map semantics are silently rewritten.

## Current observed state

| Area | Observation | Evidence class |
|---|---|---|
| Archive | 16 files; 384×384 maps; 320×320 reference crop/mask; 200×200 CPU diagnostic | `EMPIRICAL` |
| PBR structure | ORM packing is internally exact | `EMPIRICAL` |
| Iridescence | Standalone and packed mask/thickness agree | `EMPIRICAL` |
| Relief | Height and normal are flat | `EMPIRICAL` |
| Cavity/occlusion | Cavity is zero; AO is constant | `EMPIRICAL` |
| Transmission | Transmission map is constant near-full starting value | `EMPIRICAL` |
| Calibration | Numeric values are synthetic initial guesses | `HISTORICAL / PROJECT_INTERPRETATION` |
| Render parity | CPU diagnostic does not reproduce the reference rim | `EMPIRICAL` |

## Fixture identity

- **SHADER:** thin-film interference / Fresnel spectral fragment shader.
- **CANONICAL ROLE:** bubble-material research specimen and controlled visual experiment.
- **OWNED PHENOMENON:** view/light/thickness-dependent iridescence signature.
- **INPUTS:** film IOR, thickness field, wavelength range, view/light geometry, scene background, optional specimen maps.
- **OUTPUTS:** rendered color, reflectance/transmission appearance, deterministic screenshots, measured runtime behavior.
- **INVARIANTS:** source archive unchanged; map hashes stable; packed channels agree with standalone maps; reference alpha/mask parity; no unsupported calibration claim.
- **KNOWN APPROXIMATIONS:** synthetic fields; thin-shell assumptions; external background dependence; no demonstrated multiple-reflection calibration; no measured device ladder yet.
- **COUPLING LEVEL:** 1 for the current simulator: geometry/view fields modulate shader appearance. The supplied maps are not yet proven causal in the runtime.

## Decision gates

### Gate G0 — Source integrity

**Pass condition:** manifest hashes, image dimensions, and pack relationships validate in a fresh clone.
**Current:** pass in the local analysis; rerun with `python3 tests/validate_specimen.py`.

### Gate G1 — Renderer binding

**Pass condition:** the runtime loads the declared specimen maps through explicit material bindings and a capture receipt records shader/runtime hashes.
**Current:** not yet claimed. The existing runtime is a thin-film simulator; the evidence viewer exposes maps but does not bind them into the simulator.

### Gate G2 — Optical control matrix

**Pass condition:** calibration, positive, negative, and null fixtures are captured with one independent variable changed at a time.
**Current:** planned; see `docs/BUBBLE_MEMBRANE_VALIDATION_PLAN.md`.

### Gate G3 — Performance/mobile

**Pass condition:** named-device measurements cover full, reduced, and static fallback tiers.
**Current:** not measured in this branch.

### Gate G4 — Promotion

**Pass condition:** G0–G3 pass, artistic acceptance is recorded, and the material is still described with the correct evidence class.
**Current:** blocked.

## Failure and rollback policy

- If map packing fails, stop before renderer work and preserve the source archive.
- If a render differs from the reference, record the difference; do not tune values until the fixture identity and color-management state are fixed.
- If a mobile tier cannot maintain document usefulness, fall back to a poster/static image and retain the interactive runtime as opt-in.
- Never overwrite a parent specimen. New variants receive a new ID and a parent hash.

## Reviewer reconstruction

A reviewer should be able to clone the branch, run the validator, start a static server, open `docs/specimen.html`, open the simulator, and inspect this ledger plus the decision log. Every future render capture must record: fixture ID, independent variable, controlled variables, browser/GPU, viewport, source/shader hashes, output hash, and pass/fail decision.
