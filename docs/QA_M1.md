# Breakthrough M1 — technical delivery for creative review

2026-11-03, Asia/Taipei. **Bounded M1 build delivered; creative acceptance and independent first-time-player gate remain pending.** [Approved Offer](offers/BREAKTHROUGH_M1_OFFER.md), [execution authorization](decisions/M1_AUTHORIZATION.md), [play/reproduce instructions](PLAY_M1.md). Accepted Guardian R2 baseline: `f5facb1d7264e328c30b778c31b4a4cce3c64999`. Prior R2 evidence remains historical in `evidence/r2/`; this run is in `evidence/m1/`.

## Implemented behavior

The existing square 768 world now supports an independent Breakthrough scene with active bounds x192..576, the approved three-column/six-row map, three 128-unit one-hit bricks and three permanent steel blocks. Left/right lower gates are alternatives; the upper gate is offset. Two effective hits suffice. Holding Fire at spawn cannot solve it. The original Guardian range is still the default scene, with its original 64-unit walls and six-block objective.

Tank geometry, .5 scale, 156 units/s movement, immediate cardinal facing/clearance, fixed turret, unlimited one-second fire, 480-unit/s shell travel, accepted recoil and warm flash remain. Rectangular wall helpers default to 64 for the range; mission walls provide explicit 128 dimensions. Corridor boundaries consume shots and block the hull; barrel remains excluded from movement collision. Mission victory is not tied to destruction count or tank position.

One logical group uses a deterministic reverse BFS field on a 32-unit cardinal graph with a 16-unit clearance envelope. Twelve bounded decorative dots share its position; no individual AI. It waits until the entire exit route exists, then moves at 48 units/s. Effective wall destruction alone changes topology; an in-flight edge replan compares both endpoints without moving the current center. Steel hits, the tank and shells do not affect crowd occupancy. A localized waiting label identifies the initially overlapping/non-blocking crowd; route opening changes the HUD treatment, announces evacuation through the localized polite live region, and briefly outlines the group (static cue under reduced motion).

The 90-second active clock starts on explicit Start. Pause/visibility suspension preserves it; the active fraction of the current frame is settled before pausing. Slow visible frames cannot extend the deadline. Arrival is computed at first **full-envelope** containment in the exit, strictly before 90 seconds; equality loses. Late-rendered success is retained if its event preceded the deadline. Both success and timeout freeze further gameplay. Retry/replay resets map, crowd/path, shells, clock and cooldown while keeping settings. Exit and scene changes during play pause for confirmation and return to a two-exercise chooser; no campaign stages or progression.

Mission layout hides the inspector, compacts the HUD and keeps accepted controls/scene scale. Bilingual labels, mute, reduced motion, focus/keyboard behavior and storage fallback are retained. A new local-ES-module data-URL builder produces one self-contained 345,033-byte HTML. No external runtime dependencies, accounts, telemetry, APIs, new tanks, enemies, HP system, bosses, bombers or paid assets were added. Original R2 playable ZIP is unchanged; M1 has a separate review ZIP.

## Actual verification

| Check | Executed outcome and scope |
|---|---|
| `npm test` | **51 passed, 0 failed, 0 skipped:** original 24 range rules plus 27 M1 tests. The script runs both files directly, preserving named assertion counts. See `unit-tests.txt` |
| Independent path oracle | All 8 brick-removal subsets, shortest distances compared with independently written forward BFS; tie determinism under reversed wall order; synthetic mid-edge shorter-route/tie cases; continuous-center replan; sweep/corner negatives. Included in 27 M1 tests |
| Geometry/rules | All 8 map subsets sampled across positions, four initial/requested orientations, legal hull placement and turn correction<=19 units. Explicit128-unit first-hit consumption, corridor shot barrier, crowd non-blocking/non-damage, all-bricks/tank-at-exit non-win, terminal freeze and retry. Sampling is not a continuous-space proof |
| Deadline | Pure tests cover arrival before/at/after 90, center-only versus full group entry, late render of earlier arrival, long visible interval, topology change after expiry. UI tests cover entry, pause/resume, simulated hidden-tab lifecycle, exit cancel/confirmation, long-frame timeout and replay |
| `python3 tools/m1_browser.py` | **65 passed, 0 failed.** Real keyboard left solution, actual two-pointer right solution with movement+held Fire, waiting after only one gate, visible/localized evacuation cue, live language/state preservation, success/replay, timeout/retry, exit. Running non-fixture map; game state is read-only. Playwright clock controls time, not simulation state |
| Offline M1 | Same runner completes the right solution in the bundled HTML while every request except its initial document is blocked; no extra runtime network. Both entrances additionally completed against source. Direct `file://` remains unverified due managed-browser policy |
| R2 browser regression | **27 original checks and 81 focused checks passed**, outputs separated into `r2-regression/`. Includes complete range playthrough, simultaneous touch/release, storage fallback, four-direction collision/flash captures and responsive checks. No accepted test assertion disabled |
| Accessibility | axe-core 4.10.3 at 320/390/1440 widths in both languages: **0 violations**, 20 passed rules each. **color-contrast remains incomplete/manual review**. Original range audits also remain 0 violations. This is not full accessibility conformance |
| Recoil/art preservation | Source asset files, anchors, recoil function and tank draw function byte-identical to R2, recorded in `r2-preservation.json`. Current range compositor recording 174 frames /150 trace samples, sampled peak 9.48 master pixels; hull stationary. Nominal 12-pixel peak /45ms stroke /240ms recovery unchanged; sampled trace can miss exact peak under host load |
| Rebuild/package | Six local ES modules bundled with Python stdlib. Committed source archived into a separate temporary directory, builder rerun and output byte-compared: exact match. This is archive reconstruction, not a fresh GitHub clone. ZIP payload checksums and exact HTML verified; `SOURCE.json` identifies committed preview source |
| Syntax | Node syntax checks for all runtime modules; Python helpers compile. No runtime install/build dependency beyond Node/Python dev tools |

Browser evidence: managed headless Chromium 154/Linux; Python Playwright 1.62.0, Node 24.19.0. M1 viewports 320x740,390x844/DPR2 touch,768x1024,1440x900/1000,844x390; both English and Traditional Chinese. Existing range coverage includes its prior viewport/DPR matrix. Controlled browser time makes tests reproducible; it is not physical-phone performance or independent-player evidence.

Measured scripted completion active times: left keyboard 22.73s, simultaneous-touch right 21.37s, bundled right 20.77s. Only two bricks are removed; extra fired shells may hit steel/miss. These are scripted test outcomes, **not balance, fun or first-time-player results**. The provisional 90 seconds and teaching puzzle were not shortened or complicated.

## Visual and interaction review

See [evidence index](../evidence/m1/README.md). Actual 320/390 screenshots show the complete square field plus direction/Fire controls in the portrait viewport, with 44x44 direction and 94x94 Fire targets. At 320 the full page/footer may extend below the viewport. Desktop/tablet and short landscape may require scrolling; no assertion that a full-page capture fits a single screen. No horizontal overflow was measured. A first paint/resize artifact found during paused-clock screenshot verification was corrected with immediate scene/language/backing-canvas redraw; rendered brick-pixel assertions now guard against stale range imagery in mission captures.

Manual image inspection: materials remain distinct, exit is marked with text/border, crowd label/callout and persistent HUD identify the small formation; the route-open HUD and ring are restrained. Small dot separation and accepted recoil remain subtle on narrow phones. These are engineering observations, not creative-director approval. Representative palette ratios from the accepted theme remain above 4.5:1 for checked text; group pale dots versus dark disc and exit text versus dark refuge provide strong separation. Canvas-wide contrast, crowd readability and touch ergonomics still need human judgment.

## Pending gate and limitations

**Independent first-time-player test: NOT PERFORMED / NOT VERIFIED. Physical-phone test: NOT PERFORMED.** No external participant was available in this task and no message was sent to recruit one. Automated/AI playthroughs do not substitute for that gate. The next review should record device, language, attempts, completion time and confusion: can a new player identify the crowd/exit/materials, discover a route and finish by the second attempt within 90 seconds without step-by-step coaching? Owner decides whether the teaching mission communicates selective repositioning and urgency. Do not tune the timer or add mandatory targets without that evidence and further approval.

Firefox/WebKit, comprehensive screen-reader spatial gameplay, physical-device sustained performance and production-art rights remain unverified. Simulated visibility events validate handlers, not actual mobile OS background scheduling. Prototype tank provenance/licensing is unchanged and not cleared for production. No release-wide certification or live public gameplay claim.

Development branch only; no force push, merge, Pages/settings changes, paid services, public deployment or publication. GitHub workflow count/rulesets 0; Pages workflow/main source unchanged at preflight. Hook/secret metadata 403 remains unverified. See authorization for the exact constraints. Stop at creative-director Confirm & Close.

## Reproduce the evidence

From repository root, start `python3 -m http.server 8080 --bind 127.0.0.1` and use Node>=20/Python 3. `npm test` runs both rule suites. Development-only Chromium, Python Playwright 1.62.0, ffmpeg and axe-core 4.10.3 were available here; they are not game runtime dependencies.

```sh
python3 tools/build_preview.py
python3 tools/m1_browser.py
EVIDENCE_DIR=evidence/m1/r2-regression AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js python3 tools/browser_evidence.py
EVIDENCE_DIR=evidence/m1/r2-regression python3 tools/r2_browser.py
EVIDENCE_DIR=evidence/m1/r2-regression python3 tools/capture_recoil.py
python3 tools/package_m1.py
```

Set `AXE_PATH` for the M1 runner if its audit script is elsewhere. Commit the rebuilt preview before packaging; the packager checks that the archived HTML matches its stated source commit. `evidence/m1/r2-regression/tmp/` contains disposable ignored compositor frames; it is not part of the delivery.

Project lesson: explicit wall dimensions, a separate mission clock/outcome policy, and read-only state plus rendered-pixel checks let a new objective coexist with the accepted range. Default-range regression coverage is retained rather than replacing it with a new mission's passing suite. This remains a project lesson; no standards-pin change.
