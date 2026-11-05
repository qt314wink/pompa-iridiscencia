<!-- coderabbit-ai-generated:v1 -->

<!-- coderabbit-ai-generated-section:v1:2be97d07954d416b2424e8635ebe55e3399cd4bffee42b353c57a5066e3a7a4d -->

# G1 Renderer-Binding and WebGL2 Profile Receipt

<!-- coderabbit-ai-generated:v1 -->

<!-- coderabbit-ai-generated-section:v1:129380380995bfa0439c100998dafdc8aeac8690038787cd591192d4edef653e -->

**Date:** 2026-11-02

**Repository:** `qt314wink/pompa-iridiscencia`

**Base revision:**

<!-- /coderabbit-ai-generated:v1 --> `42a5066518f67000d7432c5d0be0a2390c41397b` plus [`g1_capture_runtime.patch`](g1_capture_runtime.patch)

## Executive decision

**PENDING / CALIBRATION-DEFERRED.** The packed map loaded and BASE/POS differ in this SwiftShader capture. G1-NULL and G1-NEG have not been captured, and the four controls have not been replayed. The [contract](G1_RENDERER_BINDING_CONTRACT.md) requires both before PASS-BOUND. These image-space metrics are not physical optical calibration.

## Capture environment

- WebGL2; `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)`
- Browser: `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36`
- Viewport: 1280×900 CSS pixels, device pixel ratio 1; drawing buffer: 400×350.
- Default scene and controls; BASE, POS, then BASE were read synchronously after toggling. The two BASE metrics matched.
- Texture units: 32; fragment uniform vectors: 4096.
- Frame-time p50/p95 and pixel output hashes were not captured in this run. No physical mobile GPU was measured.

## Linear image-space metrics

| Metric | G1-BASE | G1-POS | Delta POS−BASE |
|---|---:|---:|---:|
| Mean R | 0.088320 | 0.102435 | +0.014115 |
| Mean G | 0.027571 | 0.019872 | -0.007700 |
| Mean B | 0.063969 | 0.061123 | -0.002846 |
| Luma mean | 0.043114 | 0.040403 | -0.002711 |
| Luma standard deviation | 0.075302 | 0.069359 | -0.005943 |
| Non-black coverage (linear luma > 0.02) | 0.227957 | 0.214979 | -0.012979 |

Per-channel standard deviations and full precision values are in [the receipt](g1_binding_receipt.json). sRGB canvas channels are linearized before statistics are calculated.

## Reproduce this runtime state

Start from a clean checkout of the recorded base revision. Save the patch before checking out that revision, then apply it and copy the source specimen into the Pages root:

```bash
git checkout 42a5066518f67000d7432c5d0be0a2390c41397b
git apply /path/to/g1_capture_runtime.patch
mkdir -p docs/specimens
cp -R specimens/bubble_membrane docs/specimens/
python3 -m http.server 4173 --directory .
```

Open `http://127.0.0.1:4173/docs/index.html` with a WebGL2 browser at the viewport above. Wait for the specimen checkbox to become enabled. Call `window.__bubbleDiagnostics()` with the checkbox off and then on; leave other controls at their defaults. Browser, renderer and color management can affect results. Compare the hashes below before interpreting a replay.

```text
app.js: 6fc957a22ed86b1e601a9eb1e3d4056992d0d84cc85f1ce77290825f4fb850f4
shader.js: 3646487ab8ec2ef191ff1cae86eb4b6340a6bacdd4f1386ce696e4a46901e62e
specimen manifest: d4bed5b501f9165e924cca8bd57494ec2611e37775f0aa4c1e8daf9cc43b6aa8
packed RG map: c8007406155581ffc310c8bdf8265b54490b875139e17181352b288d00ed3aca
patch: 4c88a07285945e208f2f1432df599dd3df0438e5b294ac960099ddf52bb15ee7
```

## Open gates

- Capture and replay BASE, POS, NULL and NEG with matching source and shader hashes.
- Record frame-time distributions and output hashes; repeat on named WebGL2 mobile GPUs.
- Add UV orientation/seam fixture; the current binding uses object-space XY projection.
- Do not describe image-space results as physical thickness, spectral, or device performance calibration.


<!-- /coderabbit-ai-generated:v1 -->
## Control matrix and seam result

The completed browser control matrix is recorded in `docs/G1_CONTROL_MATRIX.md` and `docs/g1_binding_receipt.json`.

- **G1-NULL:** neutral 1×1 map `[0,0,0,255]`; exact pixel-statistic match to G1-BASE.
- **G1-NEG:** altered 1×1 map `[255,0,0,255]`; luma mean `0.192695` versus BASE `0.175941`, confirming causal response.
- **G1-SEAM-SWEEP:** roll angles 0–315° in 45° increments; maximum adjacent luma delta `0.000006076857`, luma range `0.000006363126`; bounded PASS at threshold `0.001`.

The seam result is limited to the roll sweep at 400×350. Elevation and geometry-remapping validation remain open.

## Spectral degradation sweep

The runtime now exposes `spectralSampleCount` for controlled 81/41/21 comparisons. At 400×350 on the same SwiftShader browser lab:

| Samples | Avg frame | FPS | Luma mean |
|---:|---:|---:|---:|
| 81 | 497.29 ms | 2.01 | 0.162193 |
| 41 | 313.11 ms | 3.19 | 0.155580 |
| 21 | 191.65 ms | 5.22 | 0.150321 |

The 21-sample approximation reduces proxy frame time by 61.4% but shifts luma by `-0.011873`; it is not promoted without an approved image-error budget.

## Actual mobile hardware gate

No physical mobile WebGL2 device was available. The browser reported Chrome 156 on Linux x86_64 with ANGLE SwiftShader. The 320×280 measurements in the receipt are reduced-resolution proxies only and must not be presented as device results.
