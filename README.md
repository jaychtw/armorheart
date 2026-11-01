# Armorheart — Guardian POC

A bounded, zero-runtime-dependency browser proving ground. **Prototype artwork, awaiting creative-director review.** No campaign, other tanks, bosses, deployment or production approval.

## Play locally

Download `preview/guardian.html`. This single file embeds the code, CSS and Guardian layers. Serve it locally using the command below, then open `/preview/guardian.html`. Its gameplay was verified with every request except the initial local document blocked. Direct double-click opening is expected in ordinary browsers but was **not verified** here: managed Chromium prohibits `file://` navigation. Browser storage may be unavailable for local files; settings then remain session-only.

For source development, from the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080` on that machine. `npm start` binds port 8080 on all interfaces for a managed local workspace preview. No external runtime requests, telemetry, accounts or credentials. The preview is not a public deployment.

Enter the range, move with arrows or WASD, and hold Space to fire. On touch, hold a direction and Fire simultaneously. Facing changes immediately, including against a barrier. Fixed turret, unlimited ammunition, 1-second cooldown. Clear the six brick blocks; steel stays. The resulting clear/replay loop is a technical exercise, not a campaign level. Pause, restart confirmation, EN/繁體中文 live switching, mute and reduced motion are available. Sound starts muted.

## Reproduce assets, checks and offline artifact

Python 3 standard library and Node >=20 are sufficient; no `npm install` is needed.

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

Use `POC_URL` and `CHROMIUM` environment variables to override the test URL/browser executable. These test utilities are not runtime dependencies. See [QA evidence](docs/QA_REPORT.md), [asset construction/provenance](assets/guardian/PROVENANCE.md), [commitment](docs/POC_COMMITMENT.md), and [current state](PROJECT_STATE.md). The exact pinned standards/GDD are in `docs/`.

Production licensing is unresolved; no blanket license to redistribute underlying artwork is asserted. Development synchronization is not human acceptance, merge or release authorization.
