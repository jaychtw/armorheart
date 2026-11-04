# Siege M4 — bounded feasibility and implementation Offer

Subsequent status: the owner accepted this Offer, Fortress direction and **both** strategies under [M4 execution authorization](../decisions/M4_IMPLEMENTATION_AUTHORIZATION.md). The bounded build is now delivered for [QA / Confirm & Close](../QA_M4.md). The original planning record below is historical and does not reopen its settled creative questions.

2026-11-04 Asia/Taipei. **Proposed; gameplay execution is not authorized.** [Owner assignment](../SIEGE_M4_OFFER_REQUEST.md) at `d66f832dab21737e54e857b98599e4e83f85b1cf`. [M3 accepted and closed](../decisions/M3_CONFIRM_CLOSE.md) at playable `108515a2f63c4818567d46de6bbcc0aa0611af07`; Guardian/R3/M2/M3 are frozen. This Offer proposes one fortress encounter, not campaign completion, unlocks or release.

**Recommendation:** two permanent central shelters, four expendable flank cells, an aimed five-round fan and a repeatable shoot/retreat rhythm. Preserve 8 fortress HP, 3 tank HP, 3-second volleys/immunity and no timer. Geometry and isolated motion support a cover-based encounter; they also expose a faster damage-trade strategy. The material creative decision is stated below rather than hidden by extra mechanics.

## Exact arena and cover

[Coordinate diagram](../../planning/siege-m4/evidence/map.svg) · [authoritative proposed data](../../planning/siege-m4/map.json). All rectangles use `(x,y,width,height)` in the unchanged 768×768 world. Guardian starts `(384,688)`, facing up. No water, enemies, random elements or damaging fortress contact.

| Object | Exact rectangle(s) | Semantics |
| --- | --- | --- |
| Fortress | `(256,64,256,160)` | Stationary solid, hittable body; 8 HP, 1 damage per player shell; no phase immunity |
| North rock | `(0,0,256,224)`, `(512,0,256,224)`, `(256,0,256,64)` | Permanent world barriers, visually rock/steel; tank and both sides' shots blocked |
| Upper bricks B0/B1 | `(256,352,64,64)`, `(448,352,64,64)` | Independent 1-HP cells; either side destroys one on effective impact |
| Lower bricks B2/B3 | `(256,544,64,64)`, `(448,544,64,64)` | Same; no linked destruction, regeneration or physical rubble |
| Upper/lower steel S10/S11 | `(320,352,128,64)`, `(320,544,128,64)` | Permanent, shown as two adjoining64-unit panels each; consume shots |

The open vertical bands are128 units from fortress to upper cover and between cover rows, then160 units below the lower row. The two outer bypasses are256 units wide. Bricks attach to the outside of each central steel mass: removing any subset creates no narrow interior slot. The permanently protected central line cannot shoot through its steel. Holding Fire at spawn delivers **zero fortress hits**.

Two choices are useful. Move to a flank and demolish its cells to open a long firing line, accepting exposure as cover disappears; or use the wider outer route into the middle court, remove its upper flank cell and alternate attacks with the permanent central shelter. The front court is a dangerous optional close approach, not a compulsory damage/precision bottleneck.

Continuous configuration-space proof covers **all16 removal states and12 nonidentical facing pairs**:119,488 certified pieces, maximum turn correction **19 units**, using the actual accepted hull and collision tolerance. Four physical routes in every state give64 unchanged-engine movement checks, with **zero route correction**. [Certificate](../../planning/siege-m4/evidence/clearance-certificate.json) · [isolated timelines/routes](../../planning/siege-m4/evidence/feasibility.json). These are assessment results, not an implemented level or browser playtest.

## Five-shell battery and cover ordering

Three fixed roof-casemate pivots are `(288,216)`, `(384,216)`, `(480,216)`. At precharge start, select the pivot nearest Guardian's x coordinate; lower index wins a tie. This keeps a flank attack exposed to its nearer battery instead of allowing a wide fortress corner to be shot safely from behind steel that blocks only a central emitter. The body does not move; only the selected short24-unit barrel tracks the tank. Its actual mouth is `pivot +24×unit(tank−pivot)`.

First launch is3.0 seconds, then6/9/12… of **active simulation time**. Precharge begins0.6 seconds earlier. Local gun/port cues and localized HUD identify the selected tracking gun; its bearing continues tracking until launch. At launch snapshot Guardian's position, fire **exactly five** rounds from that visible mouth at offsets `−30°,−15°,0°,15°,30°`, then freeze their directions. Speed180 units/s, radius4; each effective hit deals1 and consumes the round. No homing, extra attacks, HP changes or damage-stage speedups. The owner's own fortress body is excluded from its roof battery's emissions; all ordinary terrain still shields both sides.

Gaps grow with range. At240 units, adjacent angular spacing is about62.7 units; at400 it is about104.4 (`2r sin7.5°`), before subtracting the projectile diameter. A wide-facing93-unit hull cannot reliably fit the inner gap at close range. The intended answer is **retreat into central steel**, not assume every gap fits every facing. At a middle firing position `(288,480)`, the aligned center round travels about1.06 seconds before reaching the up-facing hull. A right turn/strafe clears that center line in about0.33 seconds, and right-spreading rounds meet the upper permanent steel. The inverse works on the right. Telegraphed close approaches require backing off; there is no newly added contact damage or forced visit to the gun mouth.

Cover collisions use earliest swept contact, not an endpoint-only check. A hit removes one brick and immediately consumes its shell. A later shell, including another round from the same fan, may traverse the now-empty cell. For **exactly simultaneous** contacts, evaluate all against the pre-impact wall snapshot: consume every contacting shell, remove the brick once. At equal-time ambiguity, terrain occludes an entity; stable IDs break terrain ties. Player and enemy events share chronological resolution rather than separate array orders. The accepted Guardian muzzle sweep,1-second cadence, collision, size and recoil remain unchanged.

Keep the3-second firing cadence even while an earlier round remains on screen. The isolated cover examples peak at seven live hostile rounds. A conservative world-diagonal lifetime bound is6.04 seconds, so at most three overlapping fans/15 rounds are possible before terrain clipping; no unbounded accumulation. Waiting for all rounds to leave would materially change cadence and is **not proposed**. A hit grants3 seconds of immunity to all defined damage; every colliding round is consumed even while immune. Pause/hidden freezes charge, projectiles, cooldowns and protection without a catch-up burst.

## Feasibility, attrition and the material choice

The study uses predetermined Guardian motion through the **unchanged engine**, plus isolated analytical ray/contact timelines. It has no playable M4 mission, HP/outcome controller or runtime integration. It measures the eighth target hit and contact opportunities filtered by accepted3-second immunity. These are feasibility predictions, not actual keyboard/touch victories.

| Isolated case | Measured result |
| --- | --- |
| Spawn held Fire, intact cover | No fortress hits; central steel prevents a spawn clear |
| Left/right attack-and-shelter pattern, intact map | Eighth hit23.807s, one effective contact each |
| Both patterns across all16 removal states | 32/32 reach eight hits before a third contact;20.807–23.807s, at most one effective contact |
| Limited stationary-after-approach search | 14/24 sampled position/delay cases clear before three contacts |
| Fast sampled damage-trade clear | Move left or right to the flank, then hold Fire: eighth hit10.440s, two effective contacts |

Early bricks can buy time, but hostile fire can remove them. In one intact shelter example, Guardian removes upper-left B0 at3.179s; an enemy round removes lower-left B2 at7.667s. Steel is never lost. All16 masks retain both safe shelter routes, so cover attrition changes firing exposure without eliminating recovery geography. The modeled shelter pattern first opens a flank, fires while facing up, moves inward at launch, waits until that fan passes, then returns and repeats. There is no mandatory demolition checklist: the other side's cells can remain.

**Material creative question:** is the faster “spend two HP to finish” strategy acceptable alongside the longer shelter/dodge approach, or must Siege force continued movement after setup? **Recommend retaining the initial rules for the bounded build and treating damage-free cover use as the expressive strategy**, then judging actual first-time-player behavior. Do not claim the map eliminates camping: a small relocation and sustained fire can still win. Requiring ongoing movement would need a materially different commitment, such as changed endurance/cadence or vulnerability behavior; none is authorized or silently included here. Merely moving cover cannot reliably remove the rule-level window created by an always-hittable8-HP target,1-second player fire,3 tank HP and3-second incoming opportunities. This is the Offer's principal balance limitation.

## Fortress art direction and bounded sample

[Original editable study](../../planning/siege-m4/art/fortress-study.svg) · [320px actual-scale view](../../planning/siege-m4/evidence/study-320-en-intact.png) · [390px view](../../planning/siege-m4/evidence/study-390-en-intact.png) · [Broken](../../planning/siege-m4/evidence/study-390-en-broken.png) · [Half-destroyed](../../planning/siege-m4/evidence/study-390-en-half.png) · [desktop](../../planning/siege-m4/evidence/study-1440-en-intact.png).

Propose a grounded warm-stone/olive military bastion: central keep, two raised side masses, a low front gun wall and three clearly registered casemates. Restrained elevated top-down bevels, broad surfaces and muted Guardian-compatible colors take priority over tiny masonry detail. This one original vector study evaluates mass, anchor, gun mouths and damage silhouettes; **its flatter material treatment is not a claim to match Guardian's accepted painted finish**. The proposed identity and finish need creative judgment as part of this Offer, not automatic production acceptance.

Intact8–6 retains three raised masses. Broken5–3 collapses the left upper parapet/roof and opens major cracks. Half-destroyed2–1 lowers both towers and breaks the central roof into a dark core with large rubble masses. All three casemate bases remain functional, with no behavior change at thresholds. A visibly solid full-size foundation remains at the same collision footprint in every state; collapsing roofs do not invent walk-through or transparent target gaps. Ground shadow/contact is restrained. No mutation, fantasy glow, national insignia, owner-reference copying or expensive asset suite.

Sixteen actual Chromium static-study renders cover320/390/768/1440 widths: all three preliminary states in English and an intact zh-TW view at each width. Canvas CSS width is measured from the accepted M3 game at that viewport, rather than enlarging the boss for presentation. The accepted Guardian layers/0.5 world scale are unchanged. Full foundation corners and all three muzzle pixels are checked. A static +0.5s pre-impact fan sample shows all five radius-four rounds. Cover erosion and later passage are evaluated by the separate chronological timeline, not by pretending this static still is gameplay. **These are study-page screenshots, not M4 gameplay screenshots.** [Render/registration report](../../planning/siege-m4/evidence/render-check.json).

Execution art gate: carry the chosen silhouette/ground anchor into the real renderer, refine surface/lighting integration with Guardian, register actual rotating mouths and show all damage states at320/390/1440. Keep ordinary technical corrections autonomous. If the proposed identity cannot meet the intended quality with existing $0 tools, present the smallest creative counteroffer; do not silently promote this vector study as finished art or start another broad feasibility round.

## Bounded execution proposed, once authorized

Reuse native Canvas/ES modules, existing Guardian, wall drawing, M3 circle/sweep math, combat health/protection, sound/motion settings, live localization, pause/retry/results/exit, offline compiler and evidence utilities. Add one data map and isolated Siege rule adapter; add a minimal optional solid-entity movement hook if needed so the static boss blocks movement without pretending its HP body is indestructible terrain. Default Guardian/earlier-stage paths must remain differential-equivalent. No engine/framework reconstruction or new runtime dependency.

Add **Siege · Level4 / 圍城・第四關** alongside the four existing scenes; narrow selection can use a full-width fifth button after the existing2×2 rows. Instructions explain cover erosion, fan tracking and eight-hit objective. Boss zero HP wins; tank zero loses; both return a fresh current-level state on Retry. No timer, roster, skins, unlocks, campaign progression, scoring, consumables, fortress phases, new missions, release or portfolio work. Existing historical review ZIPs remain untouched.

Implement in three practical checkpoints: rule adapter/map with targeted verification; representative real-render art/combat integration with phone checks; actual-input QA and reproducible offline review delivery. Safe development pushes only, $0, no force-push/merge/deployment/publication. Finish with source/evidence/ZIP hashes and a compact state handoff; stop for Confirm & Close.

## Acceptance evidence for that execution

- Verify exactly five launched rounds per opportunity, launch-time aim/frozen directions, all three actual mouth transforms, no hidden homing, no phase modifiers and bounded overlap. Test wall-vs-entity occlusion, two competing hits, same-time cover snapshots, later passage, shield consumption,3-second protection and terminal ordering at all HP thresholds.
- Verify all16 cover states with the actual engine and no correction above19. Demonstrate both attack/shelter directions, voluntary cover clearing, hostile cover destruction and permanent shelter through **actual keyboard and simultaneous touch inputs**. Exercise tank defeat, fortress victory, retry, exit, pause and hidden/resume. No state fixtures masquerading as playthroughs.
- Measure the fast trade-HP strategy and a cover-conscious victory in native time. Report whether observing/moving meaningfully changes survival. Do not label a finite camp search as proof that no stationary strategy exists. Disclose absent independent first-time-player/physical-device tests.
- Evaluate real M4 desktop/phone game screenshots, all damage states and charge/impact video. Confirm visual body/solid footprint, ground contact and gun-mouth registration; assess projectile contrast/spacing at320px. Art acceptance remains separate from rules passing.
- Test EN/zh-TW across all primary flows; keyboard/focus,44px targets,320/390/768/1440 and short landscape, reduced motion/mute, storage failure and appropriate axe/manual contrast review. Record incomplete canvas/nonvisual access honestly.
- Preserve all accepted Guardian/R3/M2/M3 rules, assets, proving ground and regression suites. Verify offline outcomes with subsequent requests blocked, disclose direct-file/other-engine gaps, bound particle/projectile work and record managed-browser performance without implying hardware certification.
- Deliver one playable self-contained Siege review ZIP, editable art, concise QA/evidence, clean reconstruction, verified branch SHAs and permanent GitHub links. Historical M3 tests remain reported, not independently rerun by this planning task. [Preservation check](../../planning/siege-m4/evidence/preservation.json).

[Reproduction/evidence instructions](../../planning/siege-m4/README.md) and a [clean tracked-source reconstruction](../../planning/siege-m4/evidence/rebuild-check.json) preserve the proposed geometry, editable vector master and analytical results. Four generated planning outputs rebuilt byte for byte from checkpoint `137cb17befa7adeeef89ddfce01e878b44c77b3d`; no playable M4 build is claimed.

No shared standard was changed: immutable UGDS1.0.0 `d5c6696efdd6efc028118600466db44aecae0c9b` and adopted AICP1.2.1 `b8b9de0d4faaf666fb53cec83ff8516bccf5bd5b` were read and remotely byte-verified. Current shared AICP1.5 at `a0f91837f170da97b98afe979afb473f169edf58` was read as supplemental guidance, not repinned. Original M3 reference archival remains ancillary/pending; no received bytes are claimed. **Next gate: owner review of this Offer, its visual direction and balance tradeoff, followed by explicit bounded execution authorization.**
