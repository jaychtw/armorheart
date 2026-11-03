# Interception M3 — bounded implementation Offer

2026-11-04, Asia/Taipei. **Offer for owner review; Stage 3 execution is not authorized.** [Assignment](../INTERCEPTION_M3_HANDOFF.md) · [exact map/defaults](../../planning/interception-m3/map.json) · [diagram](../../planning/interception-m3/evidence/map.png) · [continuous-turn recording](../../planning/interception-m3/evidence/route-live.webm) · [study/evidence index](../../planning/interception-m3/README.md).

The authorized Colossus presentation correction is complete and preserved at [94493a6](https://github.com/jaychtw/armorheart/commit/94493a6380f5fd34a6f56e059728c7b6ec69e21e): no battlefield Next label or separate landing ellipse, original natural shadow retained. [Corrected playable ZIP](https://github.com/jaychtw/armorheart/raw/94493a6380f5fd34a6f56e059728c7b6ec69e21e/artifacts/Armorheart-Colossus-M2-Final.zip) · [fresh QA](../../evidence/m2-final/README.md). M2 creative acceptance and its known safe-lane limitation are recorded, not reopened by this Offer.

## Commitment offered

One selectable Interception encounter: Guardian defends a peninsula against a classic, stylized battleship cruising clockwise through open sea. Six ship HP; three Guardian HP with three-second damage immunity. Predictable motion, one-damage projectiles, three-shell broadside volleys on a three-second firing clock, visible degradation, success/escape/tank-defeat/retry/exit. Preserve accepted Guardian/R3/M2 mechanics and visuals, live EN/zh-TW, keyboard/touch, reduced motion/mute and offline play. No arbitrary timer beyond the ship's actual exit.

Owner-approved peninsula geography, continuous curved turns, natural offscreen clipping and fixed starboard guns govern this proposal over earlier canal/sharp-corner interpretations. Governing [GDD](../ARMORHEART_GDD_v1.0.md) and pinned [UGDS 1.0.0](../standards/UGDS.md)/[AICP 1.2.1](../standards/AICP.md) were read; pins remain unchanged. Current shared [AICP1.5 guidance](https://github.com/jaychtw/game-development-standards/blob/a0f91837f170da97b98afe979afb473f169edf58/AI-COLLABORATION-PROTOCOL.md) was reviewed as supplemental operating guidance, not adopted over the project pin. This is $0 work on a dedicated development branch, with safe intermediate/final checkpoints. No merge, release, deployment or publication.

## Exact map and continuous route

Keep the existing **768×768 world**. Land is `[224,544] × [240,768]`, connected to the southern edge; the west, north and east are open sea. Guardian starts `(384,688)`, facing north. No destructible or steel walls in this bounded mission. Shore blocks the tank's complete accepted hull, while shells cross between land and sea. No water damage, ship ramming or new collision system.

Use a **provisional 320×88 hull**, with its pointed bow along local +X. The exact technical hull polygon and three gun anchors are in map.json. At **72 units/s**, traverse:

| Segment | Centerline | Time from start |
|---|---|---:|
| Left coast | `(112,704)` → `(112,224)`, north | 0–6.667s |
| Northwest turn | radius 144 about `(256,224)`, 180°→270° | 6.667–9.808s |
| North coast | `(256,80)` → `(512,80)`, east | 9.808–13.364s |
| Northeast turn | radius 144 about `(512,224)`, 270°→360° | 13.364–16.505s |
| Right coast and exit | `(656,224)` → `(656,928)`, south | 16.505–26.283s |

The 1,892.389-unit route has constant speed and continuous position/tangent heading: north → northeast → east → southeast → south. Each 90° corner lasts π seconds; no stop, instantaneous pivot, teleport or fog concealment. These are tangent circular fillets (C1 continuity); angular speed switches between zero and 0.5 rad/s at their joins, rather than promising a full inertial/clothoid simulation.

The hull may naturally clip at the viewport; the proxy's upper clipping reaches about 2.72 units. Its initial stern is partly offscreen, and the final stern clears y768 at the exit center `(656,928)`. Those offscreen centers are route continuation, **not extra playable world**. Player shells can hit only visible hull inside the world; no offscreen weak points or hull-size shrinkage.

[Geometry checks](../../planning/interception-m3/evidence/geometry-check.json): 7,570 route samples at 0.25-unit spacing, positive hull/land separation (68 sampled units; conservative continuous lower bound 67.47), four tangent joins, and all 64 extreme legal-center/facing cases. Guardian's worst shoreline turn correction is **19 units**, preserving its existing behavior. The common turn-safe center region is `[271.5,496.5] × [287.5,720.5]`. The art gate must rerun these checks if the actual footprint changes.

## Starboard guns and firing coherence

**Starboard is ship-right, not screen-right.** On the left coast northbound, guns point east into land; across the north coast eastbound they point south; down the right coast they point west. Reversing this traversal puts the same guns toward open sea. Choose clockwise, without independently aiming turrets or secretly reversing a leg's fire.

Three primary firing stations lie at local longitudinal offsets `−88,0,+88`, with bores/muzzles at starboard offset 66. Each volley emits one parallel shell per station, **88 units apart, speed 180 units/s, radius 4**, along the visible bore direction. No homing, spreading fan or post-launch steering. The production asset must put each flash/shell on an actual visible barrel mouth.

Recommended firing window: **hold during both turns**, and on a straight only fire if all three forward bore rays intersect land. Guns continue to rotate with the hull while holding; localized “Turning · guns holding”/alignment status explains the pause. Use a restrained **0.6-second turret charge** before an eligible volley. Diagnostic gold bore arrows in the study are not proposed gameplay lasers.

The clock ticks at 3,6,9… seconds; held ticks are skipped, never queued into a burst. Exact launches for this map/speed are **3,12,18,21s**; 6,9,15,24s hold. Thus actual gaps include 9 and 6 seconds. This is the explicitly proposed interpretation of the owner's firing-window allowance, not an undisclosed claim of uninterrupted firing every 3 seconds. The last two volleys can briefly overlap, at most six hostile shells.

A geometrically coherent curved-fire variant was also assessed. It adds diagonal volleys at 9/15s but leaves 24 sampled starts without an assessed simple escape under the 0.6s warning. That is not proof of unavoidable damage; it is unnecessary fairness/reading risk for this bounded milestone. [Rejected candidate evidence](../../planning/interception-m3/evidence/curved-fire-candidate.json). Continuous ship motion is preserved under either policy; the recommended conservative holds avoid adding diagonal combat.

## Art direction and asset gate

Classic naval hull, readable deck/superstructure and multiple heavy batteries, simplified into Guardian/transport's restrained top-down/2.5D system. Keep all main bores perpendicular toward starboard; rotate the ship and fixed battery assembly continuously as one. Propose one transparent original master/editable composition with named hull, deck/superstructure, three batteries, muzzle anchors and damage-effect layers. Reuse the existing mixed raster/vector pipeline; no multi-direction atlas or realistic naval simulation is necessary.

The [editable technical proxy](../../planning/interception-m3/ship-scale-proxy.svg), 21 [desktop/phone rotation frames](../../planning/interception-m3/evidence/render-check.json) and 26.29-second real-time recording prove geometry, registration and relative scale **only**. The supplied battleship reference was not accessible in this checkout/session; an attachment was requested once. I have not inspected it or claimed this proxy matches its identity. It must be available for a representative original art/turn sample before bulk damage-state production. Ordinary technical corrections remain autonomous; a material identity mismatch gets the smallest creative counteroffer.

At 320px viewport, this study's field is 280 CSS px: ship about 117×32px, north-facing Guardian hull about 21×34px. At 390px the field is 350px; desktop caps at 640px. Gun mouths, damage-state silhouettes and shots must remain clear there. Final ship states: **Intact 6–5, Smoking 4–3, On fire 2–1**; localized health/state labels supplement color. Smoke/fire remain restrained and attached to the ship, never hiding a turn or the targeting silhouette. No concept-sheet background or technical proxy enters the delivered game as finished art.

## Combat feasibility and risks

[Isolated model](../../planning/interception-m3/evidence/combat-assessment.json), not M3 gameplay: accepted tank hull/movement at 156 units/s, fixed cardinal turret, 1-second cooldown, 68-unit muzzle sweep and 480-unit/s player shells. The hull polygon is a technical approximation pending real artwork; swept relative collision is converged at 120/240/480Hz. These computations do not establish actual-input success or human balance acceptance.

A reproducible witness drives left for 0.675s, fires left twice before 1.9s, returns right until 2.575s, then faces north and holds Fire. Six hits win at about **12.72s**, with all three tank HP. Convergence differs by less than 0.003s. Spawn-up held Fire lands only four hits before the ship exits. A 1,568-case reachable single-station camp search (49 positions ×4 facings ×8 shot delays) found no wins, maximum five hits. It does **not** prove every possible camp is eliminated. Slower 40/56-unit speeds permit spawn-held wins, so 72 is proposed as an initial playtest value, not a proven optimum.

A separate 848-start/volley sample, including legal shoreline corners, found 394 threatened stationary states. All have an assessed zero-hit response using the 0.6s charge; 10 need moving then stopping/changing facing rather than holding one direction. [Escape study](../../planning/interception-m3/evidence/volley-escape.json). This does not certify all continuous positions, delayed reactions, overlapping volleys or physical-phone response. Closest shoreline shell contact can follow launch in about 0.23s, making the charge important.

**Remaining balance limitation:** the informed two-station witness requires positioning and two firing orientations, but little ongoing response after the initial setup. Continuous forced dodging is not guaranteed. Do not treat M2's accepted camping limitation as M3 acceptance; evaluate this specific experience in actual play. Do not silently add HP, attacks, homing, randomness, forced targets or a tighter deadline to address it.

## Implementation and acceptance boundary

Reuse the existing engine target/impact hook, Guardian rendering/recoil/input, health/immunity UI, settings, result/retry/exit and single-file packaging. Add one M3 adapter/map plus original ship assets. Separate **tank movement bounds** from **projectile world bounds**: treating sea as existing steel/bounds would wrongly stop outgoing player fire at shore. A small optional movement-bounds extension defaults to accepted behavior for every existing scene; run differential/regression checks. Use one fixed simulation clock for ship, shots and immunity, frozen by pause/hidden state; no R3 timer reuse.

Acceptance after authorization:

- Ship follows exact route/tangent heading; no coast intersection, heading snap or concealed transition. Actual hull/muzzle art agrees with geometry, including clipped corners and visible-only hit eligibility.
- Four scheduled three-shell volleys originate at real gun mouths in the matching starboard directions; held slots/status and charge are observable, with no burst or invisible projectile.
- Ship 6 HP/degradation, tank 3 HP/3s immunity, one shell/one damage/consumption, moving-target sweeps, same-frame chronological outcomes, alive-exit failure and fresh retry are verified. Exact simultaneous final-hit/exit is player-safe; later shots cannot reverse an exit loss.
- Actual keyboard and emulated-touch victories, tank defeat, missed-interception/exit and retry/exit are demonstrated. Measure informed and delayed strategies, camp witnesses and damage timings; retune only approved numeric playtest defaults with evidence, escalating core changes.
- Render 320/390/768/1440 widths in both languages, verify reachable ≥44px controls, focus/labels, mute/reduced motion, honest contrast audits and offline play. Proposed narrow chooser uses 2×2 tiles; no miniature fourth button. Disclose unperformed human/physical-device/other-engine tests.
- Fresh Guardian/R3/M2 regressions, accepted-asset/source checks, deterministic rules, reproducible preview/ZIP and permanent GitHub evidence. No production placeholder or silent visual downgrade.

Excluded: additional missions/tanks, campaign unlock/storage systems, destructible coastal scenery/cover, ship pathfinding or ramming, independent turret aiming, naval physics, extra weapons, paid resources and deployment. Deliver one bounded review build and stop for Confirm & Close.

**Next gate:** owner authorization of this bounded Offer, with the ship reference attached for art comparison. No routine engineering choice is left as an intermediate approval question. Stage3 implementation has not begun.
