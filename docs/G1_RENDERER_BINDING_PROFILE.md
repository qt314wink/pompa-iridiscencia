# G1 Renderer-Binding and WebGL2 Profile Receipt

**Date:** 2026-11-02
**Repository:** `qt314wink/pompa-iridiscencia`
**Branch:** `feat/iridlab-bubble-membrane-runtime`
**Head:** `88a7d15`

## Executive decision

**PASS-BOUND / CALIBRATION-DEFERRED.** The packed specimen map loaded in WebGL2, the G1 binding changed image-space output under the same scene state, and the source/runtime hashes are recorded. This is not physical optical calibration: the browser used SwiftShader software rendering and no named mobile GPU was measured.

## WebGL2 environment

- Context: WebGL2
- Renderer: `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (LLVM 16.0.0) (0x0000C0DE)), SwiftShader driver)`
- Vendor: `Google Inc. (Google)`
- Drawing buffer: 400×350 baseline/POS; 320×280 mobile-like proxy
- `MAX_TEXTURE_IMAGE_UNITS`: 32
- `MAX_FRAGMENT_UNIFORM_VECTORS`: 4096
- `MAX_TEXTURE_SIZE`: 8192
- `MAX_VARYING_VECTORS`: 31
- Float-linear texture support: yes
- Float color-buffer support: yes

## Optical/image-space metrics

| Metric | G1-BASE | G1-POS | Delta POS−BASE |
|---|---:|---:|---:|
| Mean R | 0.218656 | 0.228352 | +0.009697 |
| Mean G | 0.157069 | 0.135362 | -0.021707 |
| Mean B | 0.237112 | 0.233164 | -0.003947 |
| Luma mean | 0.175941 | 0.162193 | -0.013748 |
| Non-black coverage | 1.000 | 1.000 | +0.000 |

The bound map produces a visible and measurable response: mean R increases by +0.0097, mean G changes by -0.0217, and luma mean changes by -0.0137.

## Shader execution profile

The fragment shader performs an 81-sample spectral integration per fragment, with Fresnel and trigonometric work per wavelength. In this browser lab, the matched 400×350 profile measured **482.29 ms/frame baseline** and **490.68 ms/frame with G1 binding**, approximately **2.07 FPS vs 2.04 FPS**. The reduced 320×280 proxy measured **466.54 ms/frame / 2.14 FPS**, but this is not a mobile-device result.

The G1 binding adds one packed RG texture sample and map-driven thickness selection; the dominant cost remains the existing 81-iteration spectral loop.

## Hashes

```text
shader.js: 3646487ab8ec2ef191ff1cae86eb4b6340a6bacdd4f1386ce696e4a46901e62e
app.js: fa24971de1c206634fc781a1ecf780c4455b560f8e3b636a3467b07776a92ec0
specimen manifest: d4bed5b501f9165e924cca8bd57494ec2611e37775f0aa4c1e8daf9cc43b6aa8
packed RG map: c8007406155581ffc310c8bdf8265b54490b875139e17181352b288d00ed3aca
```

## Open gates

- Run G1-NULL and G1-NEG controls.
- Repeat on named WebGL2 mobile GPUs, not SwiftShader.
- Add UV orientation/seam fixture; current binding uses object-space XY projection.
- Optimize the spectral loop only after control images and lower-cost approximations are captured.
- Do not describe these results as physical thickness, spectral, or device performance calibration.
