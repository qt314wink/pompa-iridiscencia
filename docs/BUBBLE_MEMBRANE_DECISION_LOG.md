# Bubble Membrane Decision Log

## 2026-10-29 — D-001: extend existing runtime

**Decision:** Extend `qt314wink/pompa-iridiscencia` instead of creating a duplicate repository.
**Why:** It is an existing public browser WebGL simulator with a thin-film interference implementation and no open PR competing for this work.
**Rejected:** New standalone repository with a second runtime and duplicated physics context.
**Gate:** Keep the new specimen evidence viewer and source maps separate from claims about the existing simulator's shader binding.

## 2026-10-29 — D-002: preserve source specimen values

**Decision:** Copy the supplied specimen into `specimens/bubble_membrane/` without altering its scalar values or images.
**Why:** The source archive is the authority for the generated candidate and must remain reproducible.
**Rejected:** Retuning maps to match the reference before controlled renderer capture.
**Gate:** Any future tuned variant receives a new ID, parent hash, and separate acceptance record.

## 2026-10-29 — D-003: add evidence viewer before renderer binding

**Decision:** Add a static evidence viewer first.
**Why:** Reviewers need to inspect source/reference/diagnostic evidence before interpreting a new material binding as causal.
**Rejected:** Claiming the supplied maps are already driving the simulator.
**Gate:** Renderer binding is a separate G1 experiment with an explicit capture receipt.

## 2026-10-29 — D-004: use positive, negative, and null controls

**Decision:** Require calibration, positive thickness sweep, uniform-thickness null, and disabled-map negative controls.
**Why:** The reference image alone cannot distinguish thin-film structure from lighting, color management, or scene-background effects.
**Rejected:** Promoting visual similarity from one screenshot.
**Gate:** No `CANONICAL` or calibrated claim before the control matrix passes.

## 2026-10-29 — D-005: keep mobile fallback explicit

**Decision:** Preserve a static/poster fallback as a first-class release path.
**Why:** Runtime spectacle must not make the document unusable on weak devices or with reduced motion.
**Rejected:** Full shader as the only public entry path.
**Gate:** Named-device evidence required before mobile promotion.
