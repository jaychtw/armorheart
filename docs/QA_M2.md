# Colossus M2 — delivery and QA

2026-11-03 Asia/Taipei. Delivered for **creative-director Confirm & Close** on `dev/colossus-m2`. [Owner execution record](decisions/M2_AUTHORIZATION.md) supersedes the historical Offer's pending-authorization/art-pause language. Approved identity, six concepts and scale were accepted before implementation; final directional extension and build acceptance remain human decisions. [Playable guide](PLAY_M2.md) · [visual evidence and reports](../evidence/m2/README.md).

## Implemented boundary

One wall-free 768-square arena, no deadline, fixed UL(208,288) → UR(560,288) → LR(560,544) → LL(208,544) → C(384,416) → UL loop. Each stop is grounded for 2 seconds; transit is 1.2 seconds, completing a healthy cycle in 16 seconds. Four boss HP; three tank HP; grounded contact deals one damage with exactly three seconds of immunity. No extra attacks, randomness, knockback, walls, later missions or new tank mechanics. Grounded projectile vulnerability covers the visible body core; flight is invulnerable. HP changes posture/status (Intact, Fatigued, Wounded), without new mechanical phases. Chronological impact/contact resolution gives the player an exact simultaneous final-shot tie; earlier lethal contact still loses.

The optional target/impact hook extends the accepted engine for M2. Accepted hull, movement, immediate facing, scale, speed, recoil, muzzle flash and cadence are unchanged. R3 retains its separate 90-second active-time clock and both routes. M2 uses Guardian's fixed simulation clock; pause/hidden freezes phases and immunity without catch-up. EN/zh-TW health, airborne/grounded, next landing, protection and result UI, keyboard/touch, pause/retry/exit, mute and reduced motion are integrated.

## Artwork technical gate

28 original registered 448-square transparent raster frames: genuine N/rear, E, S/front-quarter and W views × idle, airborne, landing, hit, Fatigued, Wounded and look. Directional anatomy is authored, with no rotated/mirrored front bitmap. Natural brown gorilla, elevated view, planted knuckles/feet and restrained stylization follow the accepted direction; no armor, glow, snow or weapon identity. All frames and actual desktop/narrow-phone captures were inspected. [Sources/export contract](../assets/colossus/PROVENANCE.md) preserves original sheets and hashes; the editable SVG contains named raster groups, not a vector limb rig.

Common ground anchors and uniform per-direction registration retain the approved painted scale: south idle about234 world units wide. Transparent padding is not physical size. Grounded lowest pixels stay about42 world units in front of the anchor. Airborne lift is separate from crown registration. 2,420 sampled hop bounds across every view and segment remain in the arena, minimum painted margin15.67 units. Body proxies consist solely of checked opaque 4×4 blocks (alpha≥200); transparent gaps/soft fringe are excluded. Ground damage/telegraph use the distinct approved112×64 ellipse, not the sprite rectangle. Decoded frames occupy21.44MiB, below the24MiB target.

Northward diagonal hops use the rear view, horizontal travel E/W and downward travel S. Arrival view is held briefly through landing before outgoing facing. This visual mapping exposes real directional art while retaining all approved anchors and timing. Frame changes are discrete keyposes, not skeletal interpolation; small generated contour/pose differences remain visible. Technical registration checks do not establish final artistic acceptance.

## Fresh verification

| Evidence | Result and limits |
|---|---|
| `npm test` |124 passed:24 Guardian +27 historical M1 fixture +50 R3 +23 M2. M1 fixture results are not current-scene acceptance.|
| M2 actual-input browser |83 passed: real keyboard/CDP emulated touch, wins/losses, all five stops, pause/retry/exit, health/immunity, settings, bilingual layouts and offline win/loss. Controlled browser clock; snapshots read-only, no gameplay-state injection.|
| Preserved browser suites |122 R3 +81 focused Guardian +27 original range +198 visual checks =428 passed. Includes both R3 evacuation routes, all16 removal states, original range, recoil/turret occlusion and absence of truck rectangle. Some visual positive controls deliberately render the old defect.|
| Preservation |16,080 old/new full-state comparisons against accepted R3 engine, across range/all64 brick states and R3/all16 states. Frozen movement/hull/recoil/draw/flash sections, accepted assets, R3 map/navigation, old strings, standards/GDD and all four previous ZIPs match byte-for-byte. Whole extended engine is not claimed identical.|
| Art gate |28 frame/hash/proxy checks,2,420 flight-bound samples passed; registration gallery inspected.|
| Accessibility |Six axe-core4.10.3 audits at320/390/1440 widths, EN/zh-TW:0 reported violations,20 passed rules each. Canvas/color-contrast inspection remains incomplete; this is not a full accessibility-conformance certificate. Controls≥44px, keyboard and reduced motion checked.|
| Offline |Self-contained preview completes actual-input M2 win/loss with all HTTP requests except initial local HTML blocked. Fresh R3/range offline checks also pass. `file://` unverified.|
| Rebuild/package |Clean tracked-source archive recreates28 frame PNGs, manifest, proxy module and embedded preview byte-for-byte using the recorded toolchain. Deterministic ZIP, payload SHA-256 and CRC checks pass; reports linked below.|

Total browser checks:511, of which83 cover M2 directly. Reports are current executions, separate from prior historical evidence. Desktop and emulated320/390 portrait,768 tablet,1440 desktop and844×390 landscape were captured. Portrait mission HUD, canvas and Fire fit together after start; short landscape requires scrolling. No new runtime dependencies or external game requests.

## Combat measurements and balance finding

| Actual strategy | Outcome |
|---|---|
| Controlled keyboard held Fire, after driving/aiming at(560.6,698.8), up |Win7.400221 simulation seconds;5 shots/4 hits;3 tank HP; no movement after aim. Touch reproduces it.|
| Controlled keyboard four-pulse Fire |Win7.666888 seconds;4 shots;3 tank HP.|
| Live real-time Chromium touch recording |Win7.583997 simulation seconds,7.83 seconds recorded real time including tail;4 effective hits at4.150/5.150/6.568/7.584;3 tank HP; stationary after aiming at(565.8,688.4).|
| Deliberate keyboard/touch contact route |Damage at6.4,9.6,12.8 seconds; loss12.8, confirming3.2-second inter-stop contacts and continued input during immunity.|
| Live idle cycle |975 compositor frames,16.23 real seconds; five landings completed,4 boss HP/3 tank HP.|

The held-fire hits occur near3.977/4.972/6.400/7.400 seconds. Initial positioning and cardinal aiming matter, and the telegraph teaches the cycle, but **ongoing observation, dodging and reaction are not required once the safe lane is found**. This is a material engagement limitation, not a technical failure or newly granted creative acceptance. Actual play confirms the Offer's predicted safe-lane risk and is somewhat faster than its~7.8-second estimate because real silhouettes/projectile timing differ from the conservative estimate.

Isolated simulation evaluation of1.0/1.2/1.4-second flights still permits damage-free stationary victory (about7.37/7.37/8.37 seconds). It does not demonstrate meaningful engagement improvement, so shipping timing stays1.2. HP, grounded vulnerability, sequence, attacks and no-timer design are unchanged. If sustained response is essential, recommend a focused future creative decision on a telegraphed adaptive landing rule, with damage-trade testing: simply targeting landings may still allow trading under4 boss HP/3 tank HP/3-second protection. No such core change is included or automatically authorized.

## Reproduction and remaining limitations

Python3/Node24.19.0; asset export additionally uses Pillow12.3.0. Browser tools use Playwright1.62.0, Chromium154.0.8037.57, local axe-core4.10.3; recordings use ffmpeg. These are development tools, not runtime packages. No new purchase/account/API service was introduced.

```sh
python3 tools/export_colossus.py
python3 tools/check_colossus_art.py
npm test
node tools/check_m2_preservation.mjs
python3 tools/build_preview.py
python3 tools/check_m2_rebuild.py
python3 tools/package_m2.py
```

Serve source locally on127.0.0.1:8080. With `AXE_PATH` pointing to local axe.min.js run `python3 tools/m2_browser.py`; `python3 tools/record_m2.py` records real-time cycle/touch. `node tools/m2_balance.mjs` reproduces isolated timing variants. Legacy suites: `tools/r3_browser.py`, `tools/r2_browser.py`, `tools/browser_evidence.py`, `tools/visual_completion_browser.py`; set `EVIDENCE_DIR` to the corresponding `evidence/m2/r3`, `guardian`, `guardian`, `visual` folder, respectively, and provide axe. Reports and focused M2 images are committed; repeated legacy image galleries and intermediate recording JPEGs are omitted from Git.

Clean rebuild proves deterministic regeneration from preserved masters on this toolchain, not independent regeneration of AI artwork or a separately provisioned machine. Live recordings prove actual RAF/input behavior in desktop Chromium and touch emulation; they are not physical-phone or human usability tests. **No independent first-time player, physical phone, Firefox/WebKit or assistive-technology human test was performed.** Canvas gameplay still needs sight; color contrast is not fully audited. All28 images preload; low-end phone startup/memory/performance remains unmeasured. Sound starts muted; recordings do not demonstrate audio. Production licensing/provenance clearance remains unresolved; no blanket redistribution license is asserted.

R3 tank/truck pass-through remains its accepted noncritical limitation. Earlier geometry certificates remain historical; accepted geometric functions/map are unchanged and differential/regression checks above were freshly run. No merge, release, deployment, public publication, standards repin or additional mission. Budget remains$0. Stop at delivered M2 for creative-director Confirm & Close.
