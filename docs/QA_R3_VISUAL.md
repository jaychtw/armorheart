# R3 visual completion — final Confirm & Close

2026-11-03, Asia/Taipei. Reviewed baseline: `7d9720d8cee846735d5f1bb2dfc231b66eb4af7c`. The creative director accepts all reviewed R3 gameplay/presentation except barrel mounting occlusion and the truck outline; tank/truck pass-through is explicitly accepted for this milestone. This bounded correction is delivered for **final visual Confirm & Close**, not a new gameplay design or release. [Owner commitment](decisions/R3_VISUAL_COMPLETION.md) · [play guide](PLAY_R3_VISUAL.md) · [evidence index](../evidence/r3-visual/README.md).

## Corrections and exact preservation

**Barrel/turret:** assembled `tank()` drew the fixed hull/turret first and the sliding barrel second. Its mounting pixels therefore painted over the turret and stationary surface repair. The barrel is now drawn first, then the same fixed layer covers its mount. No pixels, source SVGs, anchors, recoil equation/transform, timing/amplitude/direction, muzzle code, firing interval, collision, movement or scale were changed. The forward barrel remains visible at rest and throughout recoil; all facings and size comparisons use the same assembled function. The deliberately exploded inspection remains unchanged.

**Truck outline:** `drawTransport()` explicitly stroked a134×62 light rectangle for the first two seconds after route opening. It was a departure cue, not a collision/debug overlay. That draw call alone is removed. No replacement outline was added. The localized live announcement, persistent HUD status/color change, truck artwork/body dimensions and all navigation/movement remain unchanged. The arena focus ring and exit border remain legitimate accessibility/world markings; neither encloses the truck.

[Exact-difference verification](../evidence/r3-visual/baseline-comparison.json) reconstructs these two app edits against the reviewed commit and asserts the **entire remaining app is identical**. It also hashes the unchanged engine, mission, transport planner, runtime map, i18n, all Guardian/transport assets, HTML/CSS, exact approved geometry, GDD and UGDS/AICP pins. Thus this is an authorized composition correction to the previous rendering baseline, not a recoil redesign. Previous ZIPs and historical evidence are preserved.

## Actual evidence and checks

| Verification | Outcome |
|---|---|
| Focused visual suite | **198 passed,0 failed**. Exact old-app positive controls reproduce the defect:83 incorrect overlapping pixels in its sampled right-facing shot, and the departure rectangle at desktop/320px. Corrected rendering passes all four facings at rest plus19 successive animation samples per facing at1440×1000/DPR1 and390×844/DPR2. Actual pixels where fixed layer is opaque and barrel overlaps match an independent barrel-then-fixed composition; no mount mismatches and forward barrel remains visible. Tank position remains fixed. [Results](../evidence/r3-visual/visual-results.json), [traces](../evidence/r3-visual/occlusion-traces.json). |
| Live short recording | **263 Chromium compositor frames/262 trace samples,4.369s**, actual real-time keyboard firing up/right/down/left, one shot each. Peak sampled recoil11.3925 master pixels; fixed hull throughout each recoil.200px crop enlarged3× for inspection. [Recording](../evidence/r3-visual/four-facing-live.webm), [trace/check](../evidence/r3-visual/live-recording-check.json). A separate stepped-frame clip is explicitly labeled as sampled screenshots, not live compositor capture. |
| Departure effect | Real keyboard path opens both upper cells in the actual maze. At1440px and320px, instrumented canvas stroke calls reproduce the old rectangle; corrected build has **zero truck-box strokes** in waiting, opening, moving, within and after the old two-second cue window. English/Traditional Chinese announcement and HUD remain. Actual before/after screenshots include the transition, movement and Chinese view. |
| Existing rule suites | **101 passed,0 failed/skipped**:24 current Guardian,50 current R3,27 frozen historical M1 fixtures. Includes individual one-shot damage and deterministic routing in all16 demolition states. [Output](../evidence/r3-visual/unit-tests.txt). |
| Existing R3 browser suite | **122 passed,0 failed**, freshly rerun against corrected source and corrected bundled HTML: both solutions by keyboard and emulated touch, exact2/4 shots, all16 planner states, live bilingual cue, pivots/pause, timer, timeout/retry/results/exit, reduced motion, responsive accessibility and both offline solutions. [Results](../evidence/r3-visual/r3-regression/browser-results.json). |
| Existing Guardian browser suites | **27+81 passed,0 failed**, freshly rerun: original six-brick keyboard clear/replay, simultaneous touch, storage/settings, collision/contact/turning, four-direction muzzle attachment and rendering, bilingual widths and accessibility. [Range results](../evidence/r3-visual/r2-regression/browser-results.json), [focused results](../evidence/r3-visual/r2-regression/r2-browser-results.json). |
| Layout/accessibility | Existing fresh suites cover320×740,390×844,768×1024,1440×900 and844×390;390/DPR2 used for touch. No horizontal overflow; primary targets≥44px; portrait arena/Fire within tested height. Six mission and two range axe audits have0 violations; **color-contrast remains incomplete**, not full accessibility certification. New departure captures include narrow320px. |
| Offline/reproducibility | Both mission solutions pass with every HTTP request after the initial corrected bundled HTML blocked. The delivery ZIP (222,794 bytes) passes CRC and payload-hash verification against committed preview `ed72b24f479b483581b1da0fc4a72a755d613f19`. A clean tracked-source archive rebuild passed byte-for-byte (372,065 bytes, SHA256 `ce973ae8d3cfd6879591191758f3851006ff7ec865c847bf590034f9c404e80a`). [Package report](../evidence/r3-visual/package-check.json), [rebuild report](../evidence/r3-visual/rebuild-check.json). Direct file:// remains unverified. |

The pose-only recoil fixtures replace initial tank position/facing and remove walls through HTTP routing, following the established Guardian test method. They do not change renderer, recoil, firing or input. Departure tests and full R3/range playthroughs use actual level geometry and real inputs, without mutating game state. Baseline controls load the exact reviewed app; its dependencies/assets are byte-identical. The review sheet contains unaltered actual screenshot crops, not generated artwork. Source files record the sampling/recording methods.

Existing geometric certificates remain valid evidence bound to identical map/engine/planner/envelopes; the530,944-turn and continuous19-unit-bound tools were **not rerun for this draw-only correction**. Current101 rules and browser suites do recheck all16 wall-removal/navigation states. Original geometry/results remain historical, with fresh file-identity proof supporting preservation.

## Accepted limitation and remaining gate

**Tank/truck pass-through is accepted as a noncritical limitation for this milestone.** No vehicle collision, avoidance, rerouting or displacement was added. It may be considered in a separately authorized future task and is not a required follow-up for closure.

The creative director's acceptance applies to the reviewed baseline except the two corrected defects. Final acceptance of these corrections remains pending. No independent first-time-player or physical-phone test was performed in this correction task; emulated touch is not physical-device testing. Firefox/WebKit, comprehensive screen-reader spatial play and production-art licensing remain unverified. Short landscape still scrolls. The provisional90-second clock, approved geometry and gameplay are unchanged; no balance retuning is proposed.

Branch `fix/r3-visual-completion` derives exactly from the reviewed commit. Preflight: Actions workflows0/rulesets0; Pages remains workflow/main. Prior hook/secret metadata403 remains unverified; no settings/credentials touched. Budget$0. No force-push, merge into main, deployment/publication, later missions or unrelated work. Stop for final Confirm & Close.

## Reproduce

Use existing Node≥20/Python3; no runtime package installation. Development-only tools: Python Playwright1.62.0, Chromium154, ffmpeg and axe-core4.10.3. Start loopback HTTP on8080, then:

```sh
npm test
python3 tools/build_preview.py
python3 tools/verify_visual_baseline.py
python3 tools/visual_completion_browser.py
python3 tools/record_visual_completion.py
python3 tools/make_visual_review_plate.py
EVIDENCE_DIR=evidence/r3-visual/r3-regression python3 tools/r3_browser.py
EVIDENCE_DIR=evidence/r3-visual/r2-regression AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js python3 tools/browser_evidence.py
EVIDENCE_DIR=evidence/r3-visual/r2-regression python3 tools/r2_browser.py
EVIDENCE_DIR=evidence/r3-visual python3 tools/check_r3_rebuild.py
python3 tools/package_visual.py
```

`AXE_PATH` may point elsewhere. Commit preview before packaging; the packager refuses uncommitted HTML. Clean archive reconstruction is not an independent network clone. Older `verify_r3_baseline.py` verifies the former unchanged draw order at its frozen revision; current corrections use `verify_visual_baseline.py`. Disposable frames are ignored.

Project lesson: an effect intended as a subtle departure cue can read as a collider. Prefer the retained localized HUD/status, and pair recoil-transform verification with actual fixed-layer occlusion checks. No shared standard change is proposed.
