# Armorheart — v1.0 release candidate

Four accepted tank missions, one cosmetic collection. Choose any mission, unlock Bulwark/Vanguard/Sentinel after the first three distinct victories, and earn the campaign commendation after all four. Tanks share identical accepted Guardian mechanics. Local progress, English/繁體中文, keyboard/touch, mute, reduced motion and the original training range are included. No external runtime dependencies.

## Complete-game RC1

**[Download the unified playable ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/dev/v1-finalization/artifacts/Armorheart-v1.0-RC.zip)**. Extract and open `Armorheart-v1.0-RC/index.html`, or serve the extracted folder locally. [Play guide](docs/PLAY_V1.md) · [QA](docs/QA_V1.md) · [actual screenshots and normal-speed touch campaign](evidence/v1/README.md) · [ZIP hash/manifest](evidence/v1/package-check.json) · [current state](PROJECT_STATE.md).

**183 rules and 1,285 browser assertions passed on final runs.** Four genuinely earned campaigns include keyboard, touch, offline and a 69-second normal-RAF touch recording. All 24 victory orders, exactly-once rewards, storage failures, all four cosmetic facings/recoil and prior mission regressions are covered. Initial timing/harness discrepancies are retained in QA; these are automated input runs, not independent first-time-player or physical-phone tests. All accepted gameplay/art/maps and eight earlier ZIPs are preserved.

The four individual missions are creatively accepted; this **integrated candidate and new collection await final Confirm & Close**. No merge, deployment or publication. [Proposed release/Pages handoff](docs/V1_RELEASE_HANDOFF.md) · [separate future Possibility handoff](docs/POSSIBILITY_HANDOFF.md). Existing rights, hardware/browser and canvas-accessibility limitations remain disclosed.

## Accepted Siege M4 — historical delivery

**[Download playable M4 ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/dev/siege-m4/artifacts/Armorheart-Siege-M4.zip)**. Extract and choose **Siege · Level4**. Eight-HP stationary Fortress, readable five-shot fans, four one-hit cover cells and permanent steel shelters. Both approved tactics are playable: fast HP-trading or tactical attack/retreat. The ZIP includes all four missions and the original Guardian range.

[Play guide](docs/PLAY_M4.md) · [QA and actual combat measurements](docs/QA_M4.md) · [desktop/mobile renders and native recordings](evidence/m4/README.md) · [reconstruction](evidence/m4/rebuild-check.json) · [ZIP integrity](evidence/m4/package-check.json).169 rules and815 browser assertions passed, including fresh earlier-stage checks. Native keyboard aggressive clear10.48s/one HP remaining; native touch tactical clear24.04s/two HP remaining. No independent first-time-player or physical-phone test was performed.

[Execution authority](docs/decisions/M4_IMPLEMENTATION_AUTHORIZATION.md) accepts the [Offer](docs/offers/SIEGE_M4_OFFER.md), Fortress direction and both strategies. **M4 was subsequently accepted and closed** ([record](docs/decisions/M4_CONFIRM_CLOSE.md)). No merge, deployment or publication. Earlier artifacts are preserved below.

## Interception M3 review build

**[Download playable M3 ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/dev/interception-m3/artifacts/Armorheart-Interception-M3.zip)**. Extract and choose **Interception · Level 3**. Defend the peninsula against the accepted battleship: continuous clockwise turns, fixed starboard three-shell volleys, six ship HP, three tank HP and visible damage stages. Win before the surviving ship exits. No separate countdown or new mechanics.

[Play guide](docs/PLAY_M3.md) · [QA and combat measurements](docs/QA_M3.md) · [actual desktop/mobile renders and live recordings](evidence/m3/README.md) · [ZIP verification](evidence/m3/package-check.json) · [clean reconstruction](evidence/m3/rebuild-check.json) · [continuity](PROJECT_STATE.md).

**148 rule tests and 615 browser assertions passed**, including fresh Guardian/R3/M2 preservation. Actual keyboard/touch wins take about12.7 seconds; a native-time touch recording wins in12.86 seconds without damage. The informed two-station strategy still needs little response after setup; approved combat defaults are unchanged. Independent first-time-player and physical-phone tests were not performed. Original reference ZIP/manifest archival remains pending because no file was exposed; the expected hash is recorded without claiming receipt.

[Owner implementation authorization](docs/decisions/M3_IMPLEMENTATION_AUTHORIZATION.md) supersedes the earlier planning-only restrictions. [Original bounded Offer](docs/offers/INTERCEPTION_M3_OFFER.md), [accepted editable art](planning/interception-m3/art/README.md) and historical planning evidence remain available. The ZIP contains all four scenes, offline assets and provenance. M3 creative acceptance is complete; this does not authorize merge or deployment.

## Colossus M2 accepted presentation

**[Download corrected M2 ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/fix/m2-presentation-m3-offer/artifacts/Armorheart-Colossus-M2-Final.zip)**. M2 is creatively accepted; this authorized correction removes the battlefield Next label and separate landing ellipse while keeping its natural shadow and all gameplay/art. [Play guide](docs/PLAY_M2_FINAL.md) · [before/after and fresh regression evidence](evidence/m2-final/README.md) · [acceptance record](docs/decisions/M2_FINAL_PRESENTATION.md).

The known safe-lane win is an accepted M2 balance limitation. The earlier M2 build/evidence follow for history; current Interception delivery is above.

## Colossus M2 review build

**[Download playable M2 ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/dev/colossus-m2/artifacts/Armorheart-Colossus-M2.zip)**. Choose **Colossus · Level 2**. Four-HP natural gorilla, genuine directional/registered poses, five-stop jumps, three-HP Guardian, grounded shots/contact and protection; no walls or timer. [Play guide](docs/PLAY_M2.md) · [QA and balance measurements](docs/QA_M2.md) · [live recordings and desktop/mobile evidence](evidence/m2/README.md) · [continuity](PROJECT_STATE.md).

Known balance limitation: after positioning/aiming, held Fire wins in about7.4–7.6 seconds without damage or further movement. Approved timing/HP/sequence remain unchanged. Physical-phone and independent first-time-player tests were not performed. Earlier ZIPs and evidence are preserved below.

## R3 visual completion

**[Download corrected playable ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/fix/r3-visual-completion/artifacts/Armorheart-Breakthrough-R3-Visual.zip)**. Barrel mounting now renders beneath the fixed turret with the same recoil; the truck departure rectangle is removed. [Play guide](docs/PLAY_R3_VISUAL.md) · [four-facing screenshots and short recording](evidence/r3-visual/README.md) · [QA](docs/QA_R3_VISUAL.md) · [current state](PROJECT_STATE.md).

Gameplay, source artwork, both evacuation solutions, Guardian mechanics and UI/offline framework are unchanged. Tank/truck pass-through is explicitly accepted as a noncritical limitation for this milestone; no new collision or avoidance system is added. Physical-phone and independent first-time-player tests were not performed in this correction task. Previous builds below are preserved for history.

## Previously reviewed Breakthrough R3 build

**[Download R3 ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/dev/breakthrough-r3/artifacts/Armorheart-Breakthrough-R3.zip)**. Extract and choose **Breakthrough · Level 1** in the bundled HTML. [Play guide](docs/PLAY_R3.md) · [Review sheet](docs/R3_REVIEW.md) · [QA and remaining human gates](docs/QA_R3.md) · [desktop/mobile evidence](evidence/r3/README.md) · [current continuity](PROJECT_STATE.md).

Open the exact approved S-bend maze one64-unit cell per shot. A single original covered transport takes the two-shot longer bypass or four-shot shorter shortcut automatically; steel stays. Cardinal travel/pivots, provisional90-second clock, bilingual UI, keyboard/touch, pause/retry/exit and offline play. Accepted Guardian mechanics/assets/proving ground unchanged. Both routes verified through actual keyboard and emulated touch; independent first-time-player and physical-phone tests were not performed.

## Historical Breakthrough M1 review build

**[Download Breakthrough M1 ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/dev/breakthrough-m1/artifacts/Armorheart-Breakthrough-M1.zip)**. Open the bundled HTML, choose **Breakthrough · Level 1**, then Start mission. The accepted Guardian range remains available and its original ZIP below is preserved. [M1 play instructions](docs/PLAY_M1.md) · [QA and pending human gate](docs/QA_M1.md) · [screenshots/evidence](evidence/m1/README.md).

The historical M1 build uses one crowd, two alternative lower gates and an offset upper exit gate; no enemies, 90-second deadline. M1 is delivered for creative-director review, not accepted production or a public deployment. Independent first-time-player and physical-phone tests were not performed.

## Local source preview and historical Guardian download

**[Download the playable ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/dev/guardian-review-r2/artifacts/Armorheart-Guardian-POC.zip)**, extract it, and follow the included README. See [play instructions](docs/PLAY_PREVIEW.md). This is the R2 Guardian POC preview for owner review, not a public deployment.

Download `preview/guardian.html`. This current single file embeds all five scenes, CSS, four tank cosmetics, progress/results, transport, Colossus, accepted battleship and refined Fortress artwork. Serve it locally using the command below, then open `/preview/guardian.html`. Its gameplay was verified with every request except the initial local document blocked. Direct double-click opening is expected in ordinary browsers but was **not verified** here: managed Chromium prohibits `file://` navigation. Browser storage may be unavailable for local files; settings then remain session-only.

For source development, from the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080` on that machine. `npm start` binds port 8080 on all interfaces for a managed local workspace preview. No external runtime requests, telemetry, accounts or credentials. The preview is not a public deployment.

Enter the range, move with arrows or WASD, and hold Space to fire. On touch, hold a direction and Fire simultaneously. Facing changes immediately, including against a barrier. Fixed turret, unlimited ammunition, 1-second cooldown. Clear the six brick blocks; steel stays. The resulting clear/replay loop is a technical exercise, not a campaign level. Pause, restart confirmation, EN/繁體中文 live switching, mute and reduced motion are available. Sound starts muted.

## Reproduce assets, checks and offline artifact

Python 3 standard library and Node >=20 run/build the game; no runtime `npm install` is needed. Regenerating Colossus PNG assets additionally uses Pillow12.3.0. See [v1 QA](docs/QA_V1.md) for current reconstruction, browser checks and packaging commands; [M2 QA](docs/QA_M2.md) retains its earlier asset workflow.

```sh
python3 tools/export_guardian.py
npm test
node --check src/app.mjs
python3 tools/build_preview.py
```

Edit `assets/guardian/guardian-source.svg`: its named `hull` and `barrel` groups contain masks, original embedded raster pixels and a small vector surface repair. Export again to refresh runtime SVGs. Anchors are recorded in `anchors.json` and the renderer; changes to pivots must be coordinated. This is editable mixed raster/vector source, not a fully vector-redrawn tank. The single-file preview must be rebuilt after source edits.

Browser verification (development tools only): install Python Playwright 1.62.0 and provide Chromium. Optionally install axe-core 4.10.3 in a temporary directory using npm with `--ignore-scripts`; set `AXE_PATH` to its `axe.min.js`. Start the source server, then:

```sh
POC_URL="http://127.0.0.1:8080/?inspect" AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js python3 tools/browser_evidence.py
```

Use `POC_URL` and `CHROMIUM` environment variables to override the test URL/browser executable. These test utilities are not runtime dependencies. See [current R3 QA evidence](docs/QA_R3.md), [asset construction/provenance](assets/guardian/PROVENANCE.md), [commitment](docs/POC_COMMITMENT.md), and [current state](PROJECT_STATE.md). The exact pinned standards/GDD are in `docs/`.

Production licensing is unresolved; no blanket license to redistribute underlying artwork is asserted. Development synchronization is not human acceptance, merge or release authorization.
