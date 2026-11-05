# G1 Control Matrix and Degradation Capture

**Capture date:** 2026-11-05 UTC  
**Branch:** `feat/iridlab-bubble-membrane-runtime`  
**Runtime:** WebGL2 in Chrome 156 on Linux x86_64; SwiftShader software renderer  
**Output:** 400×350 unless noted

## Control matrix

| Fixture | Independent variable | Mean RGB | Luma mean | Result |
|---|---|---|---:|---|
| G1-BASE | `specimenEnabled=false` | 0.218656 / 0.157069 / 0.237112 | 0.175941 | PASS |
| G1-POS | Immutable packed RG specimen map | 0.228352 / 0.135362 / 0.233164 | 0.162193 | PASS |
| G1-NULL | 1×1 neutral map `[0,0,0,255]` | 0.218656 / 0.157069 / 0.237112 | 0.175941 | PASS; exact match to BASE at captured precision |
| G1-NEG | 1×1 altered map `[255,0,0,255]` | 0.249455 / 0.168720 / 0.263056 | 0.192695 | PASS; causal response |

The NULL control rejects the simpler explanation that enabling the specimen branch alone changes the output. The NEG control confirms that a deliberate map change remains visible through the binding.

## UV/seam rotation fixture

The positive specimen map was rendered at roll angles `[0,45,90,135,180,225,270,315]` degrees with all other state fixed.

- Maximum adjacent luma delta: `0.000006076857`
- Luma range: `0.000006363126`
- Non-black coverage: `1.000` at all angles
- Bounded threshold used for this capture: `0.001`
- Result: **PASS-BOUND** for this roll sweep and output size.

This does not fully prove UV orientation under elevation or geometry remapping. The current projection remains object-space XY and requires a separate elevation/seam fixture before production promotion.

## Spectral sample-count sweep

| Samples | Mean RGB | Luma mean | Avg frame | FPS |
|---:|---|---:|---:|---:|
| 81 | 0.228352 / 0.135362 / 0.233164 | 0.162193 | 497.29 ms | 2.01 |
| 41 | 0.202443 / 0.134927 / 0.222168 | 0.155580 | 313.11 ms | 3.19 |
| 21 | 0.184389 / 0.133737 / 0.214278 | 0.150321 | 191.65 ms | 5.22 |

The 21-sample path reduces measured proxy frame time by 61.4% versus 81 samples, but luma shifts by `-0.011873` and the RGB distribution visibly drifts. This is an **approximation candidate**, not a promoted mobile fallback.

## Mobile hardware status

No physical mobile WebGL2 device was available to this session. The captured renderer is:

```text
ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (LLVM 16.0.0) (0x0000C0DE)), SwiftShader driver)
```

A 320×280 reduced-resolution proxy produced 2.10 FPS at 81 samples, 3.14 FPS at 41 samples, and 5.17 FPS at 21 samples. These numbers are explicitly **not** actual mobile hardware measurements.

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

The machine-readable receipt is `docs/g1_binding_receipt.json`.
