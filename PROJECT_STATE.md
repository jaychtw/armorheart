# Armorheart project state

2026-11-04 Asia/Taipei. **Interception M3 is delivered for creative-director Confirm & Close. Stop here; final M3 creative acceptance is pending.** Dedicated branch `dev/interception-m3`, derived from [owner execution authorization](docs/decisions/M3_IMPLEMENTATION_AUTHORIZATION.md) at `e58f4d0790540363c9f815c58ed7c9aa0c12a645`. Gameplay checkpoint `357f57df41fb1ba9e121b98e97155107d5181503` and verified preview/QA source checkpoint `832056783e2cc786630bf14e735b96ad3263c48a` are pushed. Accepted ship art `29c5e871f6c7b92599880b60a3666943fa452a74` is unchanged; its nonblocking imperfections do not reopen identity.

## Delivery and implemented boundary

[Playable ZIP](artifacts/Armorheart-Interception-M3.zip) · [play guide](docs/PLAY_M3.md) · [QA, reproduction and limitations](docs/QA_M3.md) · [desktop/mobile renders and native recordings](evidence/m3/README.md) · [clean reconstruction](evidence/m3/rebuild-check.json) · [package integrity](evidence/m3/package-check.json).

Exact accepted 768-square peninsula/continuous clockwise U-route, radius144 turns, 72-unit/s ship and 320×88 physical hull. Three starboard mouths at local `[-88,66]`, `[0,66]`, `[88,66]`. Six ship HP, three tank HP, three-second immunity, 0.6-second charge; eligible three-shell launches at3/12/18/21 seconds and conservative holds at6/9/15/24. Surviving-ship exit is26.283185 seconds. Tank-only shoreline bounds allow both sides' projectiles to cross the coast. No new attacks, HP, target requirements, deadline, walls or other missions; quantitative defaults unchanged.

Accepted artwork exports unchanged to an efficient 664×260 PNG (0.659MiB decoded), with editable SVG and paint masters preserved. Intact/Smoking/On-fire overlays, actual gun-mouth flashes, radius-four enemy rounds, success/tank-defeat/ship-exit/retry/level-exit, bilingual UI and keyboard/touch are integrated. Narrow portrait keeps Pause/settings/HUD/Fire accessible together; short landscape scrolls. Native Canvas/ES modules, no external runtime dependencies. The ZIP includes all four selectable scenes; range remains the default.

## Executed verification and review risks

**148 rules passed:** Guardian24, historical M1 fixture27, R3 50, M2 23, M3 24. **615 browser assertions passed:** M3 104, M2 83, R3 122, Guardian R2 81, original range27, visual corrections198. Actual keyboard and emulated-touch wins in12.676486 seconds with three tank HP; offline win12.692610 seconds. Native-time touch victory12.859114 seconds and complete route/all four volleys recorded. Both loss conditions, mobile retry/exit, live languages, pause/hidden clocks, reduced motion and blocked-network offline outcomes exercised. Native RAF median16.7ms, p95≤16.8ms in managed Chromium; not physical-device certification.

21,080 differential states match the accepted default-engine/M2 baseline. The 7,570-sample clearance certificate was rerun with the identical accepted map/equations: conservative continuous hull/shore separation67.47 units and maximum Guardian correction19. Accepted Guardian movement, hull, recoil, muzzle and cadence, R3 maze/navigation, corrected M2 shadow/presentation, all earlier assets, six prior ZIPs and historical evidence are preserved. Clean tracked-source reconstruction reproduced all five generated outputs byte for byte. Repeated packaging produced the same ZIP SHA-256: `ddec4aa4b279bf7f806f280891d1febe2c12b5c3dadbcd86a6dcc4a3d7554e60`.

The informed two-station victory still needs little response after setup. No claim of forced sustained dodging or proven enjoyable balance. The production-adapter search found zero wins in1,568 sampled stationary approaches, with at most five hits; this is not exhaustive or human testing. Do not add attacks, HP, randomness or new systems to conceal the accepted balance risk.

Physical-phone, independent first-time-player, other-engine and human assistive-technology tests were **not performed**. Six M3 axe audits reported zero violations but contrast/canvas review remains incomplete. Direct `file://` opening is unverified because managed Chromium blocks it; local HTTP with every later request blocked passed. Production licensing remains unresolved. Technical passes are not M3 creative acceptance.

## Reference handoff and accepted history

The promised `Armorheart_Interception_Original_Reference.zip` and manifest are **not exposed in this workspace/session**. [Canonical reference record](planning/interception-m3/art/references/README.md) records expected original PNG SHA-256 `68e90b405d9c35eeada65da05f27a15b3a90bfe4f0eb586ae444c09ceff25e9f` from authorization, not an independently verified received file. Archive exact original bytes/manifest when available; never substitute generated art or claim receipt. Owner authorization explicitly permits gameplay delivery despite this ancillary archival gap.

M2 is creatively accepted and corrected at `94493a6380f5fd34a6f56e059728c7b6ec69e21e`; R3 accepted runtime is `1d6abaa4f8f98bb0034641bde855ac4b16786bed`. R3 tank/truck pass-through and M2 safe lane remain accepted limitations, not new mandatory systems. Old geometry-draft stash remains untouched.

UGDS1.0.0 `d5c6696efdd6efc028118600466db44aecae0c9b` / AICP1.2.1 `b8b9de0d4faaf666fb53cec83ff8516bccf5bd5b` remain pinned. Shared AICP1.5 guidance reviewed without repinning. Budget$0; development checkpoints only. No force-push, merge, deployment/publication, paid resources or unrelated expansion. `main` remains `a70a447512b7956128dd386ef6c447fbdc801c3f`. Await creative-director Confirm & Close; no next mission is authorized.
