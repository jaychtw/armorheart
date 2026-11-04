# Interception M3 — technical review

2026-11-04 Asia/Taipei. Bounded implementation under [owner authorization](decisions/M3_IMPLEMENTATION_AUTHORIZATION.md), using the accepted [Offer](offers/INTERCEPTION_M3_OFFER.md) and ship artwork at `29c5e871f6c7b92599880b60a3666943fa452a74`. **Technical verification is complete; final M3 creative acceptance remains pending Confirm & Close.** [Play guide](PLAY_M3.md) · [screenshots and native-time recordings](../evidence/m3/README.md).

## Implemented and preserved

The exact accepted peninsula, clockwise continuous U-route, 320×88 hull, radius144 turns, 72-unit/s ship, six ship HP, three tank HP, three-second protection, 0.6-second charge and three-shell volleys are integrated. Eligible launches occur at 3/12/18/21 seconds; 6/9/15/24 opportunities hold because of turn/alignment restrictions. Surviving-ship exit is at 26.283185 seconds. No quantitative defaults were retuned and no attacks or mechanics were added.

The unchanged accepted editable SVG exports to a 664×260 transparent runtime PNG (690,560 decoded bytes). Actual ship paint uses the same continuous pose as its convex collision hull; three actual projectile origins use the registered starboard mouths. Local smoke/fire show damage without repainting identity. Shore bounds constrain Guardian, while both sides' shells cross the shore. Tank contact uses swept radius-four circles with rounded corners; moving/turning hull sweeps use bounded subdivisions. Tests cover movement reaching the shore during a tick, offscreen clipping and terminal-event order.

Guardian's accepted hull, immediate facing, correction limit, speed, scale, recoil, muzzle and one-second cadence remain unchanged. Range, R3 maze/transport and corrected Colossus remain selectable. Six earlier review ZIPs, earlier evidence, accepted source assets, GDD and standards pins remain unchanged. Native Canvas/ES modules have no external runtime dependency.

## Executed results

| Verification | Result |
| --- | --- |
| Rules | **148 passed:** Guardian24, historical M1 fixture27, R3 50, M2 23, M3 24 |
| M3 actual-input browser checks | **104 passed**, zero failures |
| Fresh earlier-stage browser suites | **511 passed:** M2 83, R3 122, Guardian R2 81, original range27, visual corrections198 |
| Total browser assertions | **615 passed** in managed Chromium |
| Baseline differential simulation | **21,080 matching states:** 16,080 range/R3 +5,000 M2 |
| Exact accepted clearance rerun | 7,570 route samples; 64 extreme tank-facing cases; conservative continuous hull/shore separation67.47 units; maximum Guardian turn correction19 units |
| Runtime art registration | Accepted SVG unchanged, transparent corners and all three opaque gun mouths verified |
| Accessibility | Six axe4.10.3 viewport/language audits, zero violations; color-contrast review remains incomplete |

See [rules](../evidence/m3/unit-tests.txt), [M3 browser report](../evidence/m3/browser-results.json), [preservation](../evidence/m3/preservation.json), [clearance](../evidence/m3/geometry-check.json) and [export registration](../evidence/m3/asset-export-check.json). The 27 M1 fixture tests retain historical coverage; they do not mean the obsolete M1 map replaced R3.

M3 source keyboard and emulated-touch playthroughs each won in **12.676486 seconds** with all three tank HP; the self-contained offline build won in **12.692610 seconds**. A full no-fire run retained a six-HP ship until its 26.283185-second escape. Actual keyboard, touch and offline defeat runs consumed all three tank HP at 21.790556 seconds and exercised immunity/input behavior. Actual touch also exercised ship-exit loss, retry and level exit. The reports cover every fired/held opportunity, rendered ship transforms, visible shell coordinates, all three damage states, pause/hidden clocks, live language changes, simultaneous two-finger controls, fresh retry and return to the range.

Desktop, 768px tablet, 390/320px portrait and short-landscape renders were inspected in both languages. Portrait M3 starts with Pause, settings, HP/status and Fire reachable together; short landscape scrolls. Touch targets meet the 44px check and there is no document-width overflow. Reduced motion removes nonessential movement/trails while keeping combat timing and readable static damage/protection feedback.

Two recordings use **unmodified native RAF and actual input**, not a virtual-clock render: [full route/all four volleys](../evidence/m3/route-live.webm) and [touch victory](../evidence/m3/touch-win-live.webm). The latter wins in **12.859114 simulated seconds /12.915328 recorded seconds**, with three tank HP. The full route records26.557244 seconds including result framing. Native RAF median was16.7ms, p95 at most16.8ms; source-ready measured232–250ms on warm loopback. These are managed-browser observations, not physical-device, cold-network or broad hardware benchmarks. [Native timing and trace metadata](../evidence/m3/recording-check.json).

M3 browser checks use actual keyboard/CDP touch, a controlled clock, read-only game snapshots and forwarding Canvas instrumentation. Earlier focused recoil/R2 suites additionally use labeled initial-state fixtures. The native recordings use neither game-state fixtures nor a virtual clock. Local HTTP offline runs block every network request after the initial bundled HTML and verify victory plus both losses; no unexpected HTTP requests or page errors were observed. Direct `file://` opening remains unverified because the managed browser blocks it.

## Balance and remaining limits

The approved informed two-station strategy still wins in about12.7–12.9 seconds without damage and requires little response after setup. This confirms the Offer's risk rather than proving sustained dodging or enjoyable balance. A [production-adapter search](../evidence/m3/balance-check.json) found **zero wins in1,568 sampled single-station approaches** (49 positions ×4 facings ×8 shot-delay phases), with at most five hits. It uses actual movement physics but is a simulation search, not player testing or an exhaustive proof. Defaults remain unchanged; adding HP, attacks, randomness or other engagement mechanics needs separate creative authority.

No independent first-time-player, physical-phone, other-browser-engine or human assistive-technology test was performed. Automated axe has an incomplete contrast review, and canvas combat cannot be treated as fully nonvisual-accessible. Production licensing remains unresolved. R3 tank/truck pass-through and the M2 safe lane remain accepted limitations; they were not promoted into new requirements.

The promised original battleship-reference ZIP/manifest is **not exposed in this session**. Its expected PNG SHA-256 is `68e90b405d9c35eeada65da05f27a15b3a90bfe4f0eb586ae444c09ceff25e9f`, supplied by the authorization, not independently verified from bytes. [Reference/provenance record](../planning/interception-m3/art/references/README.md) remains archival-pending. No substitute original or checksum claim was invented; authorization explicitly permits delivering gameplay despite this ancillary gap.

## Reproduction

Executed toolchain: Node24.19.0, Python3, Playwright1.62.0, Chromium154.0.8037.57, Pillow12.3.0, axe-core4.10.3 and ffmpeg. Browser/export tooling is development-only; runtime does not install it. Use the pinned project environment for byte-identical Chromium raster export.

```sh
python3 tools/export_m3_map.py
python3 tools/export_battleship.py
python3 tools/build_preview.py
npm test
node tools/check_m3_preservation.mjs
node tools/m3_balance.mjs
python3 -m http.server 8080 --bind 127.0.0.1
```

With the loopback server running, in another terminal:

```sh
AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js python3 tools/m3_browser.py
python3 tools/record_m3.py
```

Legacy browser utilities accept `EVIDENCE_DIR` to keep fresh evidence separate from historical reports; `EVIDENCE_DATE` is used where supported. Exact fresh reports disclose any historical hardcoded-date metadata correction. `tools/check_m3_rebuild.py` reconstructs generated outputs from a clean tracked-source archive. `tools/package_m3.py` creates and verifies the deterministic review ZIP after the preview is committed. [Clean reconstruction](../evidence/m3/rebuild-check.json) · [payload/ZIP integrity](../evidence/m3/package-check.json).

No merge, deployment, publication, expense or standards-pin change. Final review is creative-director Confirm & Close.
