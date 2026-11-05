# G1 Renderer-Binding and WebGL2 Profile Receipt

**Date:** 2026-11-05
**Repository:** `qt314wink/pompa-iridiscencia`
**Branch:** `feat/iridlab-bubble-membrane-runtime`
**Local head:** `9b23104` before final receipt refresh

## Executive decision

**PASS-NULL-POS-NEG / UV-SEAM-PASS-BOUND / MOBILE-HARDWARE-BLOCKED.** The packed specimen map loads in WebGL2, the NULL and NEG controls distinguish branch activation from map causality, and the roll-sweep seam fixture is bounded at the captured output size. No physical mobile GPU was available, so mobile promotion remains blocked.

## WebGL2 environment

- Context: WebGL2
- Renderer: `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (LLVM 16.0.0) (0x0000C0DE)), SwiftShader driver)`
- User agent: Chrome 156 on Linux x86_64
- Device pixel ratio: 1
- Drawing buffer: 400×350 for optical controls; 320×280 proxy for reduced-resolution timing
- `MAX_TEXTURE_IMAGE_UNITS`: 32
- `MAX_FRAGMENT_UNIFORM_VECTORS`: 4096
- `MAX_TEXTURE_SIZE`: 8192
- `MAX_VARYING_VECTORS`: 31

## Final-branch control matrix

| Fixture | Luma mean | Non-black coverage | Result |
|---|---:|---:|---|
| G1-BASE | 0.043114 | 0.227957 | PASS |
| G1-POS | 0.040403 | 0.214979 | PASS |
| G1-NULL | 0.043114 | 0.227957 | PASS; exact BASE match |
| G1-NEG | 0.054473 | 0.258807 | PASS; causal response |

The final branch uses the corrected linear/capture diagnostics from the remote integration commits. Earlier pre-rebase pixel metrics are superseded and must not be compared directly with this table.

## UV/seam validation

The positive specimen map was rendered at roll angles 0°, 45°, 90°, 135°, 180°, 225°, 270°, and 315° with fixed physical controls. Maximum adjacent luma delta and total luma range were both `0.000004654782`, below the bounded `0.001` threshold. This is a **PASS-BOUND** roll-sweep result, not complete UV proof. Elevation and geometry-remapping seam tests remain open.

## Spectral degradation

The runtime exposes `spectralSampleCount` and was measured at 400×350 under the same final branch:

| Samples | Mean RGB | Luma mean | Avg frame | FPS |
|---:|---|---:|---:|---:|
| 81 | 0.102435 / 0.019872 / 0.061123 | 0.040403 | 476.82 ms | 2.10 |
| 41 | 0.065880 / 0.018038 / 0.049675 | 0.030493 | 268.63 ms | 3.72 |
| 21 | 0.045427 / 0.016965 / 0.042649 | 0.024870 | 165.59 ms | 6.04 |

Twenty-one samples reduce measured final-branch frame time by 65.3% versus 81, but shift luma by `-0.015533`. This is an approximation candidate only; no image-error budget has been approved.

## Mobile hardware gate

No physical mobile WebGL2 device was available. A 320×280 SwiftShader proxy measured 2.16 FPS at 81 samples, 3.07 FPS at 41 samples, and 5.04 FPS at 21 samples. These are not actual mobile-device results. Repeat on named Android and iOS WebGL2 hardware before promoting a mobile fallback.

## Reproduction

```bash
python3 tests/validate_specimen.py
python3 -m http.server 4173 --directory .
# Open /docs/index.html
# Toggle “G1 specimen map” or use window.__bubbleControls in the browser console.
```

Machine-readable evidence: `docs/g1_binding_receipt.json`. Control details: `docs/G1_CONTROL_MATRIX.md`.

## Open gates

- Run elevation/geometry-remapping seam fixtures.
- Capture on named physical WebGL2 mobile GPUs.
- Define an image-error budget before promoting 41- or 21-sample approximations.
- Preserve the 81-sample path as the reference fixture.
