# G1 Renderer-Binding Contract

## Experiment identity

- **SHADER:** `__bubbleFragPhysical__` thin-film interference fragment shader.
- **CANONICAL ROLE:** bounded applied-material experiment; not canonical calibration.
- **OWNED PHENOMENON:** specimen-driven thickness/mask modulation of thin-film color.
- **COUPLING LEVEL:** 1 — specimen fields modulate shader material state; geometry remains the existing sphere.
- **REFERENCE STATE:** baseline shader with procedural object-space thickness.
- **INTERACTIVE STATE:** same shader with `iridlab_bubble_membrane_v0_1` packed RG map enabled.

## Controls

| Fixture | Independent variable | Controlled state | Expected result | Falsification |
|---|---|---|---|---|
| G1-BASE | specimen binding off | same camera, light, IOR, exposure, viewport | baseline spectral output | baseline cannot render or replay |
| G1-POS | specimen binding on | same state as BASE | output statistics change; mask/thickness drive a measurable color delta | bound and baseline are indistinguishable within capture noise |
| G1-NULL | binding on, mask forced to 1 | same thickness field and state | thickness remains visible without mask gating | mask path has no measurable effect |
| G1-NEG | binding on, thickness forced to 0 | same mask and state | specimen thickness contribution disappears | output remains identical to POS |

## Metrics

### Runtime metrics

- WebGL context version and renderer string (when available).
- Canvas CSS and drawing-buffer dimensions.
- `MAX_TEXTURE_IMAGE_UNITS`, `MAX_FRAGMENT_UNIFORM_VECTORS`, and float texture support.
- Shader source SHA-256, runtime source SHA-256, specimen manifest SHA-256.
- Frame-time samples and p50/p95 frame time.

### Optical calibration metrics

These are image-space diagnostics, not physical calibration:

- Mean linearized RGB of the rendered canvas.
- Per-channel standard deviation.
- Luma mean and standard deviation.
- Non-black coverage above luma 0.02.
- Difference in mean RGB and luma standard deviation between BASE and POS.
- Specimen map coverage and normalized thickness statistics.

## Promotion rule

G1 is **PASS-BOUND / CALIBRATION-DEFERRED** only if:

1. the map loads successfully and the shader compiles;
2. the binding toggle changes output under identical conditions;
3. BASE/POS/NULL/NEG captures replay with the same source and shader hashes;
4. no physical thickness or spectral calibration claim is made from image-space metrics alone.

A failed compile, absent map, or unchanged control response is a renderer-binding failure, not an optical success.
