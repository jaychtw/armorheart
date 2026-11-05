# Armorheart v1.0 RC1 — integrated verification

**Subsequent status, November5,2026:** owner accepted RC1 and separately authorized both publications; game and Possibility are now deployed and verified. [Final receipt/rollback](V1_PUBLICATION_RECEIPT.md). The following remains the historical planning/RC verification record.

2026-11-04 Asia/Taipei. [Owner finalization authority](V1_FINALIZATION_HANDOFF.md) `eb01bdb18ab1ccc5232009ccb244e1f8ca79c219`. **Four accepted missions preserved; integrated RC and new cosmetic collection delivered for final Confirm & Close, not yet creatively accepted or publicly released.** Dedicated branch `dev/v1-finalization`; runtime/preview source checkpoint [`f1a0f2379ccddbae4a3f97dd2901743ccdadec38`](https://github.com/jaychtw/armorheart/commit/f1a0f2379ccddbae4a3f97dd2901743ccdadec38). Later delivery commits add evidence/docs/package only; they do not change this runtime.

## What changed

Four freely selectable/replayable stages now share distinct-clear progress, an original four-tank cosmetic collection, three first-clear unlocks, fourth-clear campaign commendation, selected-tank persistence, completion marks and bilingual result navigation. The result medal is restrained and has manual/system reduced-motion fallback. Default product UI hides the old asset workbench; `?inspect` retains that diagnostic view. Global mute/motion remain accessible in all scenes. Locked cards and rewards explain the unlock count; no grind, points, level gating, stats or new abilities.

`src/progress.mjs` is a minimal version1 local store, isolated from every rule adapter. It validates stable mission IDs, unique completion order and earned selection; repeated victories are idempotent. Selection applies on a new attempt, never in flight. Invalid/unearned selections fall back to Guardian. Storage-denied/quota cases keep session rewards and disclose non-persistence. Corrupt JSON recovers safely; recognized pre-RC version0 migrates to1. That migration is a synthetic compatibility case, **not a claim of an earlier shipped campaign save**. Unknown future saves are left byte-preserved/read-only while this version uses session progress. No backend, sync, telemetry or third-party runtime dependency.

Bulwark/Vanguard/Sentinel have independent original constructions and silhouettes, finished with a host-native paint pass. Transparent mixed raster/vector masters, untouched archived paint/reference, exact prompt, editable transforms and layer hashes are in [provenance](../assets/tanks/PROVENANCE.md) / [manifest](../assets/tanks/manifest.json). Each uses the same accepted186×115 master hull envelope, pivot107/128, muzzle243/126 and scale0.5. The unchanged tank renderer draws the recoiling barrel below the hull. Asset CLI is absent; no canonical package/provider-job/GLB receipt is claimed.

## Executed checks

These are freshly executed results against the integrated runtime, not reused historical passes. Assertions are not counts of players or playthroughs.

| Verification | Result |
| --- | --- |
| Rules | **183 passed**: prior 169 +14 progression tests, including all 24 mission permutations, five completion counts, repeated wins, Next semantics and storage/selection edge cases |
| Integrated browser phases | **470 passed / 0 failed**: campaign172, cosmetics141, storage62, layout60, access35 |
| Fresh prior-stage browser suites | **815 passed / 0 failed**: Siege200, Interception104, Colossus83, R3 122, Guardian R2 81, original range27, visual completion198 |
| Total final browser assertions | **1,285 passed**; first-attempt discrepancies disclosed below |
| Accepted gameplay preservation | **34,080 matching differential states**, all accepted rule adapters/maps/art and eight old ZIPs byte-preserved |
| Art/registration | Four tanks transparent; three new hull alpha bounds exact; all six silhouette pairs distinct; actual four-facing rest/recoil/layer/muzzle checks |
| Clean reconstruction | **17 generated outputs byte-identical**, including six runtime layers, editable masters/PNG layers/manifest and complete HTML |
| Offline integrity | Repeated ZIP builds byte-identical; CRC/payload hashes verified; complete offline campaign with only initial HTML request |

Reports: [183 rules](../evidence/v1/unit-tests.txt), [integrated aggregate](../evidence/v1/browser-results.json), [preservation](../evidence/v1/preservation.json), [asset checks](../evidence/v1/assets/asset-check.json), [reconstruction](../evidence/v1/rebuild-check.json), [package](../evidence/v1/package-check.json), [all legacy results](../evidence/v1/README.md).

The differential certificate includes 16,080 range/R3 states and 6,000 each M2/M3/M4. Source byte comparisons freeze collision, map/route geometry, movement, recoil/draw/muzzle flash, boss rules and original M2 natural shadow; existing translations are also preserved. Only presentation/progress/controller integration changes. The all-skin physical input trace reaches exactly the same blocked-turn pose for all four tanks. No cosmetic field enters the simulation.

## Actual campaigns, controls and measured play

Three controlled-clock campaigns start with **no earned-progress or gameplay fixtures**:

- Keyboard: Siege → Interception → Colossus → Breakthrough, plus an actual repeated Siege victory. No duplicate unlock.
- CDP touch in 390px portrait: Breakthrough → Colossus → Interception → Siege. All four real wins and earned tank changes.
- Embedded offline HTML in Traditional Chinese: Colossus → Siege → Breakthrough → Interception. Every later request blocked.

That is13 actual mission victories in the three main campaigns. Each moves through the selector and progressively earned Guardian/Bulwark/Vanguard/Sentinel, checks Next/Missions/Replay, completion marks, fourth-clear commendation and reload. Controlled clock advances normal production update/render and actual keyboard/touch input; it is **not an independent human playtest**. Additional storage/layout/access cases include real wins and a real tank defeat. Five-count saves, all-earned cosmetic isolation, version migration and quota/future cases explicitly use labeled **storage fixtures**, never represented as naturally earned campaigns.

Representative controlled-clock informed clears: Siege10.45s/1HP; Interception12.69s/3HP; Colossus7.40s/3HP; R3 bypass28.19–28.21s. Fresh legacy tests also complete both R3 routes using keyboard/touch, preserve all 16 brick masks through rule coverage, M4 tactical shelter wins and all damage states/failure exits. Final M4 tactical rerun: keyboard23.80s/2HP, touch23.81s/2HP, offline26.80s/2HP. No mission parameter or balance change is made based on these timings.

[Native recording](../evidence/v1/campaign-native.webm), [native measurements](../evidence/v1/native-recording.json) and [read-only trace](../evidence/v1/native-trace.json) provide a separate normal-RAF four-mission touch campaign, earning/selecting all skins and ending with commendation. The recording uses actual Chromium compositor frames and real CDP touch in phone emulation, **no virtual clock, storage fixtures, game-state mutation or generated animation**. Observed native clears: Siege10.61s/1HP, Interception12.78s/3HP, Colossus7.47s/3HP and Breakthrough28.28s. The 69.18-second recording contains 1,957 actual frames; native RAF median/p95 were 16.7/16.7ms on this host. Exact measurements are in the report; these managed-host measurements are not physical-phone performance certification.

Four skins are rendered at rest and48ms active recoil in all four facings, with actual draw transforms checked against registered pivot/scale/muzzle and barrel-below-hull composition. Corresponding phone screenshots and physical-equivalence traces are retained. Additional320px gameplay shots prove keyboard/Enter selection, firing and native action targets. Sentinel simultaneous two-finger movement/fire is verified in Siege. Earlier visual tests retain positive controls that intentionally reconstruct old visual defects to establish detection sensitivity; those are labeled regression fixtures.

### Discrepancies and corrections during verification

The first concurrent legacy Siege attempt completed tactical touch at29.815s, outside that test's historical20–27s range, after its success/health checks passed. The unmodified test rerun passed at23.815s/2HP; no game code, tactic assertion or timing bound was loosened. The exact first-attempt cause is **not established**; input/capture timing sensitivity remains a test limitation, not a newly guaranteed duration. [Initial log](../evidence/v1/legacy/m4/initial-attempt.txt) is retained. Final green assertions do not erase that attempt.

The original-range harness's last network check initially treated `/?inspect` as a literal prefix for resource URLs, falsely calling same-origin modules external. Its check now compares parsed scheme/host, retaining real external-origin detection; the unchanged game then passed all27 checks including axe. [Initial log](../evidence/v1/legacy/range/initial-attempt.txt). This is a test-harness correction, not a runtime dependency or networking change.

## Responsive and accessibility findings

320/390/768/1440 and844×390 short landscape, EN/zh-TW, empty/full collection, all four cosmetic gameplay views, first unlock and campaign results are exercised. No horizontal overflow; action targets≥44px. In tested 320/390 portrait, Pause and Fire are visible together during play; short landscape still scrolls. Small 320px results fit all three buttons in both languages. Keyboard/Enter selects every earned tank and activates settings, Next and Missions; failure naming reflects the selected cosmetic and grants no progress. Language/settings changes and result rerenders do not mutate combat or rewards.

All 34 new and rerun axe audits report zero violations. Axe retains incomplete color-contrast/canvas review. [Numeric palette checks](../evidence/v1/contrast-check.json) cover six declared UI pairs, ratios5.44:1–11.79:1, including locked labels and reward/commendation text. The assistant inspected actual desktop/phone collection,320px Chinese result and all-skin gameplay-scale examples for distinct silhouettes, clear recoil/muzzle layering, crop/targets and readable hierarchy. Enlarged asset charts are labeled inspection only, not substituted for gameplay scale. This does not certify every changing canvas pixel, nonvisual play or real assistive technology. System/manual reduced motion and mute are tested; sound starts muted. No unrelated accessibility redesign or new mechanic was added.

## Artifact, static audit and remaining limits

Self-contained HTML: **10,958,341bytes**,15 local modules. ZIP: **7,573,900bytes**, SHA-256 **`6afd0bb8771494e96d9625e23f74e76e13c486061d8ace702849c5d7ad4ec466`**. Extraction yields `Armorheart-v1.0-RC/index.html`, player guide, source/hash manifest and six provenance files. Source preview checkpoint is f1a0f237; final Git delivery SHA is separately verified. Byte-identical clean reconstruction starts from an empty `git archive`, archived paint and accepted assets; it does not regenerate image-model output from a prompt or claim cross-toolchain identity.

[Local static prefix check](../evidence/v1/static-check.json) covers `/armorheart/`, a native actual M2 victory, earned Bulwark selection, Chinese and reload with only initial HTML requests. [Read-only policy audit](../evidence/v1/release-audit.json) and [proposed release plan](V1_RELEASE_HANDOFF.md) document Pages feasibility/current settings. [Separate Possibility handoff](POSSIBILITY_HANDOFF.md) follows actual current portal conventions. Neither project nor portal was merged/deployed/published; no workflow/service was activated and no release/tag made. Budget remains$0; existing permissions/provenance caveats are not erased by static feasibility.

**Not performed:** independent first-time-player, physical-phone, Safari/Firefox/other-engine or human assistive-technology testing; direct `file://` opening is blocked by the managed browser. Full canvas contrast/nonvisual support remains incomplete. Progress is browser/device/origin-local, no cloud sync or concurrent-tab transactional merge. Accepted limitations remain: R3 tank/truck pass-through, M2 stationary safe lane, M3 informed two-station finish and M4 aggressive HP-trading strategy. No timer/HP/attack changes. Production licensing remains unresolved; original M3 reference bytes/manifest remain unavailable and are not claimed received. Final composed-game creative acceptance and separate release authority are pending.

## Reproduction

Node≥20 and Python3 standard library run/build the game; no runtime `npm install`. Asset reconstruction additionally uses Pillow12.3.0, Playwright1.62.0 and Chromium154.0.8037.57; axe4.10.3 and FFmpeg are development tools only. Start a loopback source server on8080. Then:

```sh
npm test
node tools/check_v1_preservation.mjs
python3 tools/check_collection_assets.py
python3 tools/v1_browser.py
python3 tools/check_v1_rebuild.py
python3 tools/check_v1_static.py
python3 tools/record_v1.py
python3 tools/package_v1.py
```

`V1_PHASE=campaign|cosmetics|storage|layout|access` runs one focused browser phase. Aggregate reports include a runtime hash and accept only matching phases. For each legacy browser tool set `EVIDENCE_DIR=evidence/v1/legacy/<stage>` to avoid overwriting historical evidence; basic range additionally uses `POC_URL=http://127.0.0.1:8080/?inspect` and `AXE_PATH=/tmp/armorheart-audit/node_modules/axe-core/axe.min.js`. Run native recordings/performance observations without concurrent browser suites. Raw frame caches and duplicate legacy screenshot galleries are excluded from Git. Packaging refuses an uncommitted runtime preview and compares repeated ZIP bytes.
