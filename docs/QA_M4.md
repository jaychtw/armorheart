# Siege M4 — technical review

2026-11-04 Asia/Taipei. **Playable bounded M4 delivered for creative-director Confirm & Close; final composed-build acceptance is pending.** [Owner authorization](decisions/M4_IMPLEMENTATION_AUTHORIZATION.md) at `ce298580273e34da872f1d99e5150edbcc109c12` accepts the [Offer](offers/SIEGE_M4_OFFER.md), Fortress direction and both aggressive/tactical strategies. [Play guide](PLAY_M4.md) · [actual screenshots and native-time recordings](../evidence/m4/README.md).

## Delivered scope and integrity

The exact approved768×768 map is integrated: stationary256×160 Fortress at `(256,64)`,8 HP; Guardian at `(384,688)`,3 HP/3s immunity; four independent64-unit brick cells, two permanent central128×64 shelters and northern permanent barriers. All five scenes are selectable, including the preserved Guardian range and accepted R3/M2/M3. No roster, unlocks, campaign progression, timer, extra attack or phase-based mechanic was added.

Each3-second opportunity emits five180-unit/s, radius-four rounds at `−30°,−15°,0°,15°,30°`. A0.6-second charge locks the nearest of three roof guns; the selected24-unit barrel tracks until launch, then projectile bearings freeze. Collision, muzzle flash and actual barrel use the same gun pose. Both sides consume shells at first cover/entity contact. Independent bricks disappear immediately; later shells can pass. Exact-time impacts see a shared pre-impact cover snapshot; all contacting shells are consumed and each brick is removed once. Terrain occludes entities on a tie; exact simultaneous final boss/tank hits are player-safe. There is no contact/ram damage.

A small optional solid-entity movement hook and projectile delegate keep shared Guardian turning, movement, one-second firing, muzzle sweep and recoil authoritative while Siege resolves both sides' projectiles chronologically. Earlier stages do not activate these hooks. Movement is traced at156 units/s until a clamp rather than treating a turn correction as swept travel. Rounded circle/hull and circle/wall contacts avoid square-corner phantom hits. Pause/hidden freezes active combat time without a catch-up burst.

The approved Fortress study remains unchanged. The refined editable SVG adds deterministic material wear, bevel lighting and consistent stone/olive finish. Three512×320 body PNGs preserve a fully opaque physical foundation through Intact8–6, Broken5–3 and Half-destroyed2–1; gun barrels are separate rotating layers with mounting caps above them. No copied concept image or new paid asset/service is used. [Provenance/registration](../assets/fortress/PROVENANCE.md). Final art quality remains a creative judgment, separate from registration checks.

Runtime/preview source checkpoint: [`baf61ba9be766d39b03486694d73654685371d1b`](https://github.com/jaychtw/armorheart/commit/baf61ba9be766d39b03486694d73654685371d1b). [Clean reconstruction](../evidence/m4/rebuild-check.json) recreated **nine generated outputs byte for byte**, including all three body PNGs, editable master, gun layers, anchors, exact map module and10,434,219-byte embedded HTML. The final playable ZIP is7,231,453 bytes; repeated builds matched SHA-256 `b7290fee472213bc13d252c1adcf7062ef4628c03d303ad560482a0e31e8ec9e`. CRC, payload checksums and identity with the browser-tested preview were verified. [Package manifest/check](../evidence/m4/package-check.json).

## Executed results

| Verification | Result |
| --- | --- |
| Rules | **169 passed:** Guardian24, historical M1 fixture27, R3 50, M2 23, M3 24, M4 21 |
| M4 actual-input/render browser assertions | **200 passed**, zero failures |
| Fresh prior-stage browser assertions | **615 passed:** M3 104, M2 83, R3 122, Guardian R2 81, original range27, visual regressions198 |
| Total browser assertions | **815 passed**, not815 playthroughs |
| Preserved default engine / prior adapters | **28,080 matching differential states:**16,080 range/R3 +6,000 M2 +6,000 M3 |
| Full continuous turning certificate | All16 cover masks/12 nonidentical facing pairs;119,488 certified pieces; maximum correction19 units |
| Production-adapter tactical partial-cover cases | **32/32** left/right examples reach victory over all16 masks;20.807–23.807s, at least two tank HP retained |
| Body/asset registration | Three distinct fully opaque physical foundations; accepted study unchanged; all three actual rendered gun tips checked |
| Automated accessibility | Six axe4.10.3 viewport/language audits, zero violations; contrast/canvas review remains incomplete |

[Rule output](../evidence/m4/unit-tests.txt) · [M4 browser report](../evidence/m4/browser-results.json) · [clearance](../evidence/m4/clearance-certificate.json) · [preservation](../evidence/m4/preservation.json) · [asset pixels/hashes](../evidence/m4/asset-check.json). The27 historical M1 fixture tests do not mean the obsolete M1 layout replaced accepted R3.

Rule tests cover exact data/stages/solid footprint, locked precharge and launch-time aim, five-shell/cadence/overlap, independent player/enemy destruction, permanent steel, same-time snapshot consumption, earlier deletion/later passage in one frame, terrain occlusion, instant muzzle contact position,3s immunity with usable controls, both tactical directions across all masks, aggressive wins, actual tank defeat, final-hit chronology, terminal freeze/fresh retry, bounded indefinite-play traces and invalid intervals. No earlier art, map, rule adapter, localization string or any of seven earlier ZIPs changed. Guardian hull/recoil/draw/flash and the corrected Colossus natural shadow are frozen; default engine/adapter states were independently compared with the accepted M3 baseline.

## Actual play and timing

| Input/evidence | Aggressive finish / HP left | Tactical finish / HP left |
| --- | --- | --- |
| Controlled-clock actual keyboard |10.452917s /1 |23.803750s /2 |
| Controlled-clock actual CDP touch |10.452917s /1 |23.803750s /2 |
| Self-contained offline HTML |10.452917s /1, zh-TW |23.803750s /2 |
| Native-clock recording |10.480833s /1, keyboard |24.041667s /2, CDP touch |

The full clips record10.699345/24.282535 seconds including result framing. Both approved speed/survival tradeoffs are preserved without numeric retuning. These are observed runs, not optimal/guaranteed clear times; input/phase differences can require an additional opportunity. An earlier native touch recording attempt ended in defeat during the scripted retreat. The recorder's route was revised to restore the middle-court standoff using ordinary controls; **no game mechanics changed**. Only completed final recordings are counted as passed. The shelter approach rewards maintaining space; point-blank gun approaches remain risky and unnecessary. No new anti-camping requirement is proposed.

Actual keyboard, touch and offline no-fire defeat occurs at17.308334s with three effective contacts and reset/exit exercised. Actual-input victories show player and enemy cover loss; steel remains. A separate actual oblique approach selects and fires the right roof gun; Canvas forwarding measurements compare all three barrel/muzzle transforms and every visible hostile round with the collision state. Both languages are checked through live switching, HUD, entry, Chinese offline victory/defeat and retry. Simultaneous two-finger movement/fire, charge, protection, pause/hidden, restart/cancel, level exit, mute and reduced motion were exercised. Tests read snapshots; no M4 initial-state fixtures or state setters are used in these browser playthroughs.

The32 all-mask tactical cases are **rule-adapter tests**, not32 actual-input or human playtests. Focused older R2/recoil browser suites use explicitly labeled initial-state fixtures; historical visual positive controls intentionally recreate old defects. Those are distinct from unmodified M4 playthroughs and native recordings.

## Render, accessibility, performance and offline limits

Actual desktop,320/390px phone,768px tablet and844×390 landscape screenshots cover English/zh-TW. Portrait starts with Pause/settings/HUD/Fire reachable together,44px targets and no document-width overflow. The fifth narrow selector spans the final row. Short landscape scrolls. Reduced motion suppresses nonessential smoke shifts/shot trails, with static charge/health feedback retained. The refined damage silhouettes, ground contact, mounted barrels and projectile positions were inspected in actual screenshots; this assistant review is not owner artistic acceptance.

Native recordings use unmodified RAF/compositor, actual keyboard/CDP touch, and no game-state fixtures or virtual clock. Both measured16.7ms median and p95; maximum16.8ms. Source-ready was185–212ms on warm loopback. Body textures add1.875MiB decoded memory plus two small shared gun layers. World clipping bounds hostile lifetime below6.04s, at most15 overlapping rounds by geometry; production traces/history are bounded. These observations describe managed Chromium, not physical-device, cold-network or broad hardware certification.

All network requests after the initial bundled HTML were blocked during offline victories and defeat; no unexpected external HTTP requests or page errors were observed. Direct `file://` opening remains **not verified** because managed Chromium blocks it. The ZIP remains self-contained with a documented local-HTTP fallback. Existing local settings/storage fallback and accepted regression coverage are retained; no new progress data is stored.

**Not performed:** independent first-time-player, physical-phone, other-browser-engine or human assistive-technology testing. Axe reports zero violations but a serious incomplete color-contrast review; canvas play is not certified fully nonvisual-accessible. Production licensing remains unresolved. Accepted prior limitations remain: R3 tank/truck pass-through, M2 safe lane and M3 informed two-station finish. The original M3 owner-reference ZIP/PNG/manifest is still unavailable; expected hash is recorded without claiming receipt. These are disclosed limits, not new mechanics or silent passes.

## Reproduction and stopping point

Executed environment: Node24.19.0, Python3.12, Playwright1.62.0, Chromium154.0.8037.57, Pillow12.3.0, axe-core4.10.3 and ffmpeg. No external runtime dependencies. Tools/browser packages are development-only; retain the same Chromium for byte-identical raster exports.

```sh
python3 tools/export_m4_map.py
python3 tools/export_fortress.py
python3 tools/build_preview.py
npm test
node tools/check_m4_preservation.mjs
python3 tools/check_m4_clearance.py
python3 tools/check_fortress_assets.py
python3 -m http.server 8080 --bind 127.0.0.1
```

With that server running, from another terminal:

```sh
AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js python3 tools/m4_browser.py
python3 tools/record_m4.py
python3 tools/check_m4_rebuild.py
python3 tools/package_m4.py
```

The package tool requires the preview to be committed. Legacy browser tools accept `EVIDENCE_DIR`/`EVIDENCE_DATE`; fresh earlier-stage reports are isolated under `evidence/m4/legacy/` so historical evidence is preserved. The ordinary range runner also uses `AXE_PATH` for its two audits. Do not run native performance capture concurrently with other browser suites. Raw JPEGs and repeated legacy PNGs are excluded from Git.

Pinned UGDS1.0.0/AICP1.2.1 remain unchanged; shared AICP1.5 was reviewed without repinning. Budget$0. No merge, deployment, publication, release, paid resource or scope expansion. Deliver this review build and **stop at creative-director Confirm & Close**.
