# G1 Control Matrix and Degradation Capture

**Capture date:** 2026-11-05 UTC  
**Branch:** `feat/iridlab-bubble-membrane-runtime`  
**Runtime:** WebGL2 in Chrome 156 on Linux x86_64; SwiftShader software renderer  
**Output:** 400×350 unless noted

## Final-branch control matrix

| Fixture | Independent variable | Mean RGB | Luma mean | Non-black coverage | Result |
|---|---|---|---:|---:|---|
| G1-BASE | `specimenEnabled=false` | 0.088320 / 0.027571 / 0.063969 | 0.043114 | 0.227957 | PASS |
| G1-POS | Immutable packed RG specimen map | 0.102435 / 0.019872 / 0.061123 | 0.040403 | 0.214979 | PASS |
| G1-NULL | 1×1 neutral map `[0,0,0,255]` | 0.088320 / 0.027571 / 0.063969 | 0.043114 | 0.227957 | PASS; exact match to BASE |
| G1-NEG | 1×1 altered map `[255,0,0,255]` | 0.123430 / 0.030582 / 0.088083 | 0.054473 | 0.258807 | PASS; causal response |

The NULL control rejects the simpler explanation that enabling the specimen branch alone changes the output. The NEG control confirms that a deliberate map change remains visible through the binding.

## UV/seam rotation fixture

The positive specimen map was rendered at roll angles `[0,45,90,135,180,225,270,315]` degrees with all other state fixed.

- Maximum adjacent luma delta: `0.000004654782`
- Luma range: `0.000004654782`
- Non-black coverage remained approximately `0.215` at all angles.
- Bounded threshold used for this capture: `0.001`
- Result: **PASS-BOUND** for this roll sweep and output size.

This does not fully prove UV orientation under elevation or geometry remapping. The current projection remains object-space XY and requires a separate elevation/seam fixture before production promotion.

## Spectral sample-count sweep

| Samples | Mean RGB | Luma mean | Avg frame | FPS |
|---:|---|---:|---:|---:|
| 81 | 0.102435 / 0.019872 / 0.061123 | 0.040403 | 476.82 ms | 2.10 |
| 41 | 0.065880 / 0.018038 / 0.049675 | 0.030493 | 268.63 ms | 3.72 |
| 21 | 0.045427 / 0.016965 / 0.042649 | 0.024870 | 165.59 ms | 6.04 |

The 21-sample path reduces final-branch frame time by 65.3% versus 81 samples, but luma shifts by `-0.015533` and the RGB distribution drifts. This is an **approximation candidate**, not a promoted mobile fallback.

## Mobile hardware status

No physical mobile WebGL2 device was available to this session. The captured renderer is:

```text
ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (LLVM 16.0.0) (0x0000C0DE)), SwiftShader driver)
```

A 320×280 reduced-resolution proxy produced 2.16 FPS at 81 samples, 3.07 FPS at 41 samples, and 5.04 FPS at 21 samples. These numbers are explicitly **not** actual mobile hardware measurements.

## Reproduction

```bash
python3 tests/validate_specimen.py
python3 -m http.server 4173 --directory .
# Open /docs/index.html
# Use browser console:
JSON.stringify((window.__bubbleControls.setFixture('NULL'), window.__bubbleControls.setSampleCount(81), window.__bubbleControls.capture()))
JSON.stringify((window.__bubbleControls.setFixture('NEG'), window.__bubbleControls.setSampleCount(81), window.__bubbleControls.capture()))
JSON.stringify((window.__bubbleControls.setFixture('POS'), window.__bubbleControls.setSampleCount(81), window.__bubbleControls.rotationSweep()))
```

The machine-readable receipt is `docs/g1_binding_receipt.json`. The final source hashes are recorded there and must be checked before replay.
