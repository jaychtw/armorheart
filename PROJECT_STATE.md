# Armorheart project state

2026-11-04 Asia/Taipei. **Siege M4 playable review build delivered; stop for creative-director Confirm & Close. Final composed M4 acceptance is pending.** Branch `dev/siege-m4`, based on [owner execution authority](docs/decisions/M4_IMPLEMENTATION_AUTHORIZATION.md) at `ce298580273e34da872f1d99e5150edbcc109c12`. The owner accepted the Fortress direction and both fast HP-trade/tactical shelter strategies; do not reopen them or add anti-camping mechanics. Verified runtime/preview source checkpoint `baf61ba9be766d39b03486694d73654685371d1b`. Fetch and verify the current branch tip before resuming.

[Playable M4 ZIP](artifacts/Armorheart-Siege-M4.zip) · [play guide](docs/PLAY_M4.md) · [QA/measurements/reproduction](docs/QA_M4.md) · [native recordings and actual screenshots](evidence/m4/README.md) · [clean reconstruction](evidence/m4/rebuild-check.json) · [package integrity](evidence/m4/package-check.json).

## Implemented and verified

Exact approved map/8-HP stationary Fortress, three selectable registered gun mouths, aimed non-homing five-round fans every3s,0.6s precharge, four independent one-hit bricks, permanent steel shelters/northern barriers,3-HP Guardian/3s protection. Original refined editable stone/olive art has Intact/Broken/Half-destroyed silhouettes with the same solid footprint. Success/death/retry/exit, EN/zh-TW, keyboard/simultaneous-touch, pause/hidden, reduced motion/mute and offline bundle are integrated. No timer, extra attack/phase, roster, unlocks or campaign progression. All four missions plus Guardian range are selectable.

**169 rules and815 browser assertions passed** (200 M4 +615 fresh earlier-stage checks). Production-adapter tactical cases pass in both directions over all16 cover masks; continuous turning certificate retains the accepted19-unit bound.28,080 differential states match accepted range/R3/M2/M3 behavior. All earlier art/maps/adapters/localizations, seven prior ZIPs and historical evidence are preserved.

Actual keyboard/touch/offline aggressive wins10.45s with one HP left; tactical wins23.80s with two HP left. Native recordings: keyboard10.48s/one HP; touch24.04s/two HP. Defeat/retry/exit, all damage states, five-shot/muzzle alignment including oblique right gun, bilingual results, phone controls and offline outcomes are exercised. An initial native touch replay failed; the recorder route was revised to restore middle-court spacing through ordinary inputs, without game changes. Independent first-time-player and physical-phone tests were not performed.

Clean tracked-source reconstruction recreated nine outputs byte for byte. The self-contained ZIP is7,231,453 bytes, SHA-256 `b7290fee472213bc13d252c1adcf7062ef4628c03d303ad560482a0e31e8ec9e`; repeated builds/CRC/payload hashes match. Native RAF median/p95 both16.7ms in managed Chromium, not hardware certification. Six M4 axe audits report zero violations with incomplete contrast/canvas review. Other engines, human assistive-technology, direct-file opening and production licensing remain unverified; short landscape scrolls. See QA for methods and limits.

## Accepted history and boundaries

[M3 accepted/closed](docs/decisions/M3_CONFIRM_CLOSE.md) at `108515a2f63c4818567d46de6bbcc0aa0611af07`; M2 accepted/corrected `94493a6380f5fd34a6f56e059728c7b6ec69e21e`; R3 accepted runtime `1d6abaa4f8f98bb0034641bde855ac4b16786bed`. Guardian hull/movement/scale/cadence/recoil/muzzle and original range are preserved. Prior R3 overlap/M2 safe-lane/M3 fast informed-win limitations remain accepted, not follow-up requirements. Old geometry stash untouched.

Original M3 reference ZIP/PNG/manifest bytes are still unavailable; [canonical provenance](planning/interception-m3/art/references/README.md) records expected hash, not receipt. Archive exact bytes if actually supplied; do not claim recovery or block this delivery.

UGDS1.0.0 `d5c6696efdd6efc028118600466db44aecae0c9b` and adopted AICP1.2.1 `b8b9de0d4faaf666fb53cec83ff8516bccf5bd5b` remain pinned; supplemental shared AICP1.5 read without repinning. Budget$0, safe development checkpoints only. No force-push, merge, deployment/publication, paid resource, next mission or unrelated expansion. Project deployment and Possibility publication remain **not started / not authorized**. Main remains `a70a447512b7956128dd386ef6c447fbdc801c3f`. Await creative-director Confirm & Close.
