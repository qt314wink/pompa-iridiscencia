# Bubble Membrane Validation Plan

## Goal

Determine whether the specimen provides a reproducible iridescence capability beyond a simpler uniform material, while separating map packaging, renderer binding, optical appearance, and device cost.

## Fixture matrix

| ID | Role | Independent variable | Controls | Expected signature | Null/falsification |
|---|---|---|---|---|---|
| CAL-00 | Calibration baseline | Material complexity: none | Camera, light, exposure, tone mapping, output size | White dielectric sphere is stable and repeatable | Non-deterministic baseline blocks all later claims |
| POS-01 | Positive control | Known thickness sweep | Same geometry, IOR, light, camera | Spectral color bands move with thickness/view angle | No change under sweep means mechanism is not observable |
| NULL-01 | Simpler null | Uniform thickness replacing field | Same shader and scene | Spatial banding collapses or becomes uniform | If indistinguishable from POS-01, field adds no demonstrated value |
| NEG-01 | Negative control | Mask/thickness disabled | Same scene and geometry | Iridescence signature disappears | Persistent bands indicate an uncontrolled scene/renderer source |
| MAP-01 | Packaging | Standalone vs packed maps | Same sampling/filtering | Equal channel values after unpacking | Mismatch blocks renderer binding |
| SEAM-01 | UV robustness | Object rotation / tiled repeat | Same map and material | No unexpected seam or orientation artifact | Seam error defers promotion |
| MOB-01 | Degradation | Full → reduced → static fallback | Named device and viewport | Document remains useful at each tier | Long tasks, blank render, or lost hierarchy fail tier |

## Capture receipt fields

```text
fixture_id
claim_class
independent_variable
controlled_variables
geometry_and_uv
renderer_and_browser
gpu_or_device
viewport_and_pixel_ratio
source_manifest_sha256
shader_hash
output_sha256
metric_and_threshold
observed_result
falsification_condition
promotion_decision
```

## Proposed thresholds

These are targets, not achievements until measured:

- Deterministic replay: same fixture and source hashes produce the same captured state.
- Accessibility: all essential controls keyboard reachable; reduced motion retains hierarchy.
- Runtime: no blank/failed canvas at the supported baseline; static fallback always available.
- Interaction: no long task over 50 ms during the controlled interaction capture on the named baseline device.
- Mobile: document usefulness is preserved before interactive enhancement.

## Next experiment order

1. Run G0 source validation.
2. Add explicit specimen-map binding behind a documented runtime flag.
3. Capture CAL-00, POS-01, NULL-01, and NEG-01 under identical color management.
4. Add SEAM-01 and verify object-space/tangent-space conventions.
5. Measure MOB-01 on a named desktop and mobile device.
6. Record artistic acceptance and decide whether the specimen is `DEFER`, `APPLIED`, or eligible for a later canonical gate.
