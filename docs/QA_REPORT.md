# Guardian R2 — verification and owner review

2026-11-03 (Asia/Taipei). **R2 technical delivery for Confirm & Close; new visual acceptance pending.** [Owner authorization](decisions/R2_AUTHORIZATION.md), [implementation decisions](decisions/R2_IMPLEMENTATION.md), [preflight](decisions/R2_PREFLIGHT.md). Prior POC report is preserved in [QA_REPORT_POC.md](QA_REPORT_POC.md); prior evidence in `evidence/` is historical, current evidence in `evidence/r2/`.

## What changed

Artwork-derived93x57.5 hull/track collider rotates with the sprite and excludes the barrel. Movement clamps to physical wall boundaries without overshoot or step-size gaps. Immediate turning uses minimum center clearance when a rotated hull would intersect a wall; maximum geometric expansion19 world units. Owner selected wall-placement changes instead of large narrow-gap relocations. All six bricks and six steel barriers remain, with new clearance layout; speed156 units/s, scale.5, start center and projectile mechanics unchanged. All64 brick-removal combinations are sampled to ensure destruction does not recreate narrow turn traps. This is still one proving ground, not a campaign.

Original procedural transparent muzzle effect combines Q-1C-inspired direction with warm forward bloom; narrow root follows the actual recoiling muzzle, all four directions, existing90ms lifetime. No supplied opaque checkerboard pixels or concept background imported. Original CSS steel plates/rivets/seams on page with pale work surfaces. Text contrast strengthened. Wall fragmentation explicitly **deferred**, unchanged acceptable effect.

Accepted recoil function, draw transform, source SVGs/layers and anchors are byte-identical to recovered baseline `cfb1bd3b7529286ef10083e57df478b1c77898b6`. Flash attachment corrects its own origin without changing recoil. Prototype asset licensing remains unresolved; no production rights are implied.

## Executed checks

| Check | Actual outcome / limit |
|---|---|
| `npm test` |24 passed,0 failed,0 skipped: original11 scenarios retained (geometry/layout-dependent premises adapted),13 focused hull/contact/turn/corner/projectile/map regressions added. `evidence/r2/unit-tests.txt` |
| `node tools/check_map_clearance.mjs` |657,152 legal turn samples across all64 brick-removal subsets, four initial/requested facings;24-unit spatial grid. Maximum sampled correction17.5 units, regression ceiling19. Sampling is not continuous-space proof. `map-clearance.json` |
| `AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js python3 tools/browser_evidence.py` |27 passed,0 failed. Actual keyboard six-brick clear/replay, pause, preferences/storage fallback, EN/zh-TW, real simultaneous two-touch input and release, responsive/reduced-motion checks, no external requests/JS errors. New valid route replaces a route that relied on undersized collision. `browser-results.json` |
| `python3 tools/r2_browser.py` |81 passed,0 failed. Both wall types, four approaches at desktop1440 and phone390/DPR2, stable contact, blocked turns, parallel movement/adjacent corners, all-direction flash frames and320/390/1440 bilingual theme captures. Fixture HTTP routing replaces initial scene data only; unchanged production physics/rendering/input handle real keyboard events. Actual SVG opaque pixels are rasterized independently and checked against wall interiors. `r2-browser-results.json` |
| Accessibility |axe-core4.10.3 desktop/mobile zh-TW:0 violations,24 passed rules each; **color-contrast incomplete**, not full conformance. Representative text palette ratios5.11–9.54:1; Fire label7.41:1; manual screenshot inspection. `contrast-review.json`, `axe-*.json` |
| `python3 tools/capture_recoil.py` |175 compositor frames;150 transform samples; peak11.3925 master pixels; hull stationary. Byte-identical recoil/layers/transform comparison recorded separately. `guardian-recoil.webm`, `recoil-render-trace.json`, `recoil-baseline-comparison.json` |
| Offline preview |Rebuilt self-contained HTML; actual shot destroys a brick with all additional requests blocked, no JS errors. `offline-preview-check.json`. Direct `file://` opening remains unverified due managed-browser policy |
| Syntax/helpers |Node syntax checks on changed modules and Python helper compilation passed. No runtime libraries/install step |

Browser: headless Chromium154 on managed Linux; Node24.19.0; Python Playwright1.62.0. Existing suite covers320x740,390x844/DPR2,768x1024,844x390,1440x900/DPR2 plus desktop playthrough. Focused suite adds1440x1000 and390x844/DPR2. The desktop idle90-frame sample remains limited host evidence, not physical-phone performance proof. Current screenshots are generated from the running revised renderer; controlled fixture shots are identified separately from full-layout screenshots.

## Review order / evidence

1. Collision: `evidence/r2/collision-{1440,390}-{brick,steel}-{up,right,down,left}.png` and `collision-corner.png`. Hull stays clear; barrel may extend over wall. Rectangle encloses small protrusions/transparent corners conservatively; wall art is inset1–2 world units from logical boundary. No pixel-perfect claim.
2. Flash: `flash-{1440,390}-{brick,steel}-{up,right,down,left}.png`. Brick may already be destroyed in firing frame; steel remains. Warm jet direction/root and readability require owner judgment. The blast is original procedural prototype art, not the supplied bitmap or accepted production art.
3. Theme: `theme-{320,390,1440}-{en,zh-TW}.png`, ordinary desktop/mobile suite screenshots. Page seam treatment is static, no runtime requests. Inspection shows no horizontal overflow or new control overlap. Narrow-phone primary scene and controls still require vertical page navigation; short landscape still requires scrolling. No claim that whole page fits one screen.
4. Frozen recoil: comparison JSON, trace, recording and unchanged source. Phone recoil remains subtle by owner-approved baseline; not redesigned.

## Remaining gates and limitations

Creative-director acceptance of R2 collision feel, flash, layout and theme is **pending**. The owner's acceptance of prior recoil and acceptable wall breakup is recorded separately from new visual approval. Physical-phone testing, Firefox/WebKit, independent players, comprehensive screen-reader gameplay and canvas contrast remain unverified. Production licensing/provenance/naming is not cleared. No campaign, other tanks, bosses, unlocks, services, paid resources or standards changes added.

Pre-push: no Actions workflows/rulesets; workflow-based Pages remains unchanged. Webhook/secret metadata403, unverified. Dedicated development checkpoints only, no force push. GitHub source preservation, tests, visual acceptance, CI and release are distinct; no CI success, merge, deployment, publication or live public gameplay is claimed.

## Reproduce

From repository root, use Node>=20 and Python3. `npm test`; `node tools/check_map_clearance.mjs`; `python3 tools/build_preview.py`. Start `python3 -m http.server 8080 --bind 127.0.0.1`. For development-only browser evidence, install Playwright1.62.0 and Chromium; axe-core4.10.3 is optional to the runner but was supplied for this report. Execute the browser commands above, then `python3 tools/capture_recoil.py`. Both browser scripts use local port8080. `python3 tools/package_preview.py` creates deterministic playable ZIP with source commit and payload checksums; commit the updated preview before packaging so SOURCE.json names its actual source revision.

## Project lesson

An abstract collider test can pass while rendered artwork penetrates a wall. Pair artwork/pivot/scale validation with actual-render pixel checks and real-input contact demonstrations. Test cardinal-turn clearance after obstacle destruction, not only on the intact map. Recorded as project evidence; no universal standards change proposed.
