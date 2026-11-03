# Armorheart — Guardian / Breakthrough / Colossus

A bounded browser prototype with no external runtime dependencies. Guardian and Breakthrough R3 are accepted; Colossus M2 is delivered for **creative-director Confirm & Close**. Guardian range remains the default scene. No public deployment or production-art approval.

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

## Play locally

**[Download the playable ZIP](https://github.com/jaychtw/armorheart/raw/refs/heads/dev/guardian-review-r2/artifacts/Armorheart-Guardian-POC.zip)**, extract it, and follow the included README. See [play instructions](docs/PLAY_PREVIEW.md). This is the R2 Guardian POC preview for owner review, not a public deployment.

Download `preview/guardian.html`. This current single file embeds all three scenes, CSS, Guardian layers, transport and Colossus artwork. Serve it locally using the command below, then open `/preview/guardian.html`. Its gameplay was verified with every request except the initial local document blocked. Direct double-click opening is expected in ordinary browsers but was **not verified** here: managed Chromium prohibits `file://` navigation. Browser storage may be unavailable for local files; settings then remain session-only.

For source development, from the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080` on that machine. `npm start` binds port 8080 on all interfaces for a managed local workspace preview. No external runtime requests, telemetry, accounts or credentials. The preview is not a public deployment.

Enter the range, move with arrows or WASD, and hold Space to fire. On touch, hold a direction and Fire simultaneously. Facing changes immediately, including against a barrier. Fixed turret, unlimited ammunition, 1-second cooldown. Clear the six brick blocks; steel stays. The resulting clear/replay loop is a technical exercise, not a campaign level. Pause, restart confirmation, EN/繁體中文 live switching, mute and reduced motion are available. Sound starts muted.

## Reproduce assets, checks and offline artifact

Python 3 standard library and Node >=20 run/build the game; no runtime `npm install` is needed. Regenerating Colossus PNG assets additionally uses Pillow12.3.0. See [M2 QA](docs/QA_M2.md) for the full reproduction commands.

```sh
python3 tools/export_guardian.py
npm test
node --check src/app.mjs
python3 tools/build_preview.py
```

Edit `assets/guardian/guardian-source.svg`: its named `hull` and `barrel` groups contain masks, original embedded raster pixels and a small vector surface repair. Export again to refresh runtime SVGs. Anchors are recorded in `anchors.json` and the renderer; changes to pivots must be coordinated. This is editable mixed raster/vector source, not a fully vector-redrawn tank. The single-file preview must be rebuilt after source edits.

Browser verification (development tools only): install Python Playwright 1.62.0 and provide Chromium. Optionally install axe-core 4.10.3 in a temporary directory using npm with `--ignore-scripts`; set `AXE_PATH` to its `axe.min.js`. Start the source server, then:

```sh
AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js python3 tools/browser_evidence.py
```

Use `POC_URL` and `CHROMIUM` environment variables to override the test URL/browser executable. These test utilities are not runtime dependencies. See [current R3 QA evidence](docs/QA_R3.md), [asset construction/provenance](assets/guardian/PROVENANCE.md), [commitment](docs/POC_COMMITMENT.md), and [current state](PROJECT_STATE.md). The exact pinned standards/GDD are in `docs/`.

Production licensing is unresolved; no blanket license to redistribute underlying artwork is asserted. Development synchronization is not human acceptance, merge or release authorization.
