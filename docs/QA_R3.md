# Breakthrough R3 — technical delivery for Confirm & Close

2026-11-03, Asia/Taipei. **Bounded R3 implementation delivered for creative-director review; creative acceptance pending.** [Authorization](decisions/R3_AUTHORIZATION.md) · [approved geometry](offers/BREAKTHROUGH_R3_VERIFIED_GEOMETRY.md) · [play instructions](PLAY_R3.md) · [evidence index](../evidence/r3/README.md).

## Result and preserved baseline

The exact approved S-bend/shortcut map replaces the M1 gates/dots. Four independent 64×64 bricks are one hit each; five steel cells remain permanent. The original editable covered transport has a recognizable cab, bonnet, windshield/mirrors, bumper/lights, spare tire, three axles, canvas bows/ties and restrained camouflage. No reference pixels, paid assets or external runtime dependencies were added.

The visible body, including tires/mirrors/bumpers, is 128×56. Cardinal navigation uses a 136×64 padded envelope, radius76 pivot disc, speed48 units/s and 0.35-second quarter-turns. Stable travel-time Dijkstra evaluates position and heading. Each forward action checks its swept padded rectangle; each pivot checks the whole disc. New demolition during an action replans at its next legal endpoint without a jump. Transport is non-blocking and shot-immune as approved. Full visible body containment **and north-facing orientation** decide exit, strictly before 90 active seconds. Waiting→evacuating uses a two-second restrained body outline, persistent HUD change and localized live announcement; it does not flash or depend on sound.

Guardian engine, all Guardian assets, tank draw and muzzle-flash code are byte-identical to M1. The original six-brick proving ground, movement, geometry, scale, speed, immediate facing, recoil and firing remain unchanged. HTML/CSS shell and reusable M1 real-time clock/pause/retry/exit UI are retained. [Baseline hashes](../evidence/r3/baseline-comparison.json) bind these claims to M1 `bfd228359fbf56f03f921cb3d3439c7c26ed5c79`; approved map bytes match `026fb7a68b6a2e6ae18c11e38fee6a75e8d9c931`.

## Executed verification

| Check | Actual result and evidence |
|---|---|
| `npm test` | **101 passed**, 0 failed/skipped:24 accepted Guardian rules,50 current R3 rules,27 frozen historical M1 fixture rules. Historical gate/dot fixtures are explicitly separate from current R3 coverage. [Output](../evidence/r3/unit-tests.txt) |
| R3 real-input Chromium | **122 passed**,0 failed: keyboard bypass/shortcut, emulated-touch bypass/shortcut, simultaneous direction+Fire, exact2/4 shots, individual-cell/partial-state screenshots, all16 production navigation states, route cue, timed pivots/pause, live localization, retry, timeout, exit/cancel, hidden-event lifecycle, five viewport sizes, six axe audits, both offline routes and no JS/external-network errors. [Results](../evidence/r3/browser-results.json) |
| Original Guardian input/render | **27+81 passed**,0 failed. Actual six-brick keyboard clear/replay and two-finger direction/fire; R2 contact/turn/flash pixel checks, both wall types/all facings at desktop/mobile, bilingual layouts, storage/settings/reduced motion. Controlled R2 fixtures replace initial data over HTTP only; production physics/renderer/input unchanged. [27 results](../evidence/r3/r2-regression/browser-results.json), [81 results](../evidence/r3/r2-regression/r2-browser-results.json) |
| Exact-map Guardian assessment rerun | **530,944 actual-engine turns**, worst sampled15.5 units; approved preparation routes max13.5. Old47.59 witness now15.5. Continuous certificate: **192 facing cases,203,200 pieces,0 failures, bound19**, tolerance1e-7. All16 demolition subsets included. [Fresh reports](../evidence/r3/geometry/) |
| Transport all16 states | Independent Python geometry oracle rerun and current Node/Chromium planners agree. Reachable iff U0+U1 removed; one lower cell never unlocks shortcut. Bypass976 units/5 pivots/**22.0833s**; shortcut656/3/**14.7167s**. Swept-body/disc checks and1-degree padded corner checks; minimum extra disc clearance4. [Oracle](../evidence/r3/geometry/transport-results.json), [Chromium](../evidence/r3/browser-all16.json) |
| Granular damage all16 states |50-rule R3 suite includes every remaining brick in every subset: a shot from a legal Guardian pose removes exactly that cell, leaves all steel, and does not pierce the island. Also covers deferred replans, strict90-second boundaries, full-body goal, tank/shot nonblocking, terminal freeze and clean retry. |
| Actual truck artwork | Chromium raster alpha bounds exactly256×112 source →128×56 world; padded corner radius75.153<76. Four-facings inspection plate; production-driven pivot frames independently rasterized against surviving wall interiors:0 opaque overlap in checked frames. Circle/swept-envelope checks cover intermediate motion; pixel tests are selected actual frames, not every frame. [Footprint](../evidence/r3/art-footprint.json), [plate](../evidence/r3/transport-four-facings.png) |
| Original range geometry/recoil |64 range demolition subsets/657,152 turns, max17.5;150 recoil samples/174 compositor frames, peak11.3925 master pixels, fixed hull. New [recording](../evidence/r3/r2-regression/guardian-recoil.webm), trace and [clearance](../evidence/r3/r2-regression/map-clearance.json). |
| Accessibility/layout | EN/zh-TW at320×740,390×844/DPR2 touch,768×1024,1440×900,844×390. No horizontal overflow; direction/Fire targets≥44px; arena/Fire within tested portrait heights. Six mission axe audits:0 violations,20 passed rules each; **color-contrast incomplete**. Range desktop/mobile audits also0 violations. Reduced motion honored; clock/pivot pause verified. This is not comprehensive accessibility certification. |
| Offline/artifact | Self-contained preview plays **both** routes with all subsequent HTTP requests denied; range fires/destroys a brick under the same restriction. ZIP manifest checks actual committed preview and payload hashes. Clean tracked-source archive reconstruction must match the committed HTML byte-for-byte; see package/rebuild reports in evidence. |

These are new runs on this R3 instance. Earlier M1/Guardian reports remain historical, not substituted for R3 evidence. The reference geometry reports remain preserved in planning; fresh engine report also records the old witness replay. The browser harness now waits for an observed facing rather than assuming a20ms input pulse contains a rendered update; this changes only test synchronization.

Keyboard bypass finished at28.205s active mission time, shortcut22.031s; emulated touch28.214s/22.024s. Offline runs28.212s/22.004s. These are scripted informed routes with controlled time, **not first-time-player balance evidence**. Keep the provisional90-second deadline. The optional extra two shots save about7.367s of truck travel; discovery/aiming costs still require playtesting.

## Creative review and remaining limits

**Independent first-time-player test: NOT PERFORMED. Physical-phone test: NOT PERFORMED.** No outside participant was recruited or tested. Browser input is real Playwright keyboard/CDP touch into Chromium; mobile sizes/DPR are emulated. Visibility tests dispatch lifecycle events, not real mobile OS backgrounding. Firefox/WebKit, physical sustained performance, comprehensive screen-reader spatial play and production-art licensing are unverified. Direct `file://` opening is blocked by managed-browser policy and not verified; loopback HTTP with all extra requests denied is verified.

Review truck identity/materials at phone size, camouflage contrast, pivot feel, maze readability and route discovery without coaching. A first-time player should identify truck/refuge/materials, discover a viable route and finish by a second attempt within90 seconds; record device/language/attempts/time/confusion. Large transport and Guardian intentionally do not block one another and can visually overlap; judge that presentation. Short landscape still needs scrolling and phone recoil remains subtle as accepted. Do not tune the timer, resize vehicles, change Guardian mechanics or add mandatory targets without further approval/evidence.

Original Guardian provenance remains unresolved for production. Transport is newly authored prototype vector art using supplied U-1/W-1 as concepts only, not a blanket production-rights claim. See [transport provenance](../assets/transport/PROVENANCE.md).

## Reproduce

Node≥20 and Python3 suffice for runtime/build/unit checks; no npm install. Development evidence additionally used Python Playwright1.62.0, Chromium154, ffmpeg and axe-core4.10.3. These are not game dependencies. Start `python3 -m http.server 8080 --bind 127.0.0.1`, then:

```sh
npm test
python3 tools/build_preview.py
python3 tools/verify_r3_baseline.py
node planning/r3-geometry/verify_engine.mjs
python3 planning/r3-geometry/certify_clearance.py
python3 planning/r3-geometry/verify_transport.py
python3 tools/r3_browser.py
EVIDENCE_DIR=evidence/r3/r2-regression AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js python3 tools/browser_evidence.py
EVIDENCE_DIR=evidence/r3/r2-regression python3 tools/r2_browser.py
EVIDENCE_DIR=evidence/r3/r2-regression python3 tools/capture_recoil.py
node tools/check_map_clearance.mjs
python3 tools/package_r3.py
```

`AXE_PATH` can point elsewhere. `check_map_clearance.mjs` retains its historical default output under evidence/r2; copy its fresh report into the R3 folder. Geometry tools output to planning; compare/copy reports without replacing prior evidence. Commit preview before packaging. M1 browser/packaging scripts target its historical map and must run from its frozen revision, not the R3 runtime. Disposable frame files are ignored. Playwright controls time; playthroughs never mutate game state.

No spend, force-push, main merge, deployment/publication or later missions. Dedicated `dev/breakthrough-r3` checkpoints only. CI/deployment preflight:0 workflows/rulesets; Pages workflow/main unchanged; webhook/secret metadata403 unverified. A development push is preservation, not human acceptance or a release. Stop at creative-director Confirm & Close.
