# Breakthrough Level 1 — bounded M1 implementation Offer

2026-11-03, Asia/Taipei. **Proposed; awaiting execution commitment. Assessment and planning only.**

## Authority and feasibility conclusion

Assignment: [owner's Offer request at b4bf8ca](https://github.com/jaychtw/armorheart/blob/b4bf8ca28706775e7004486a30c958dd05f28c57/docs/BREAKTHROUGH_M1_OFFER_REQUEST.md). Accepted technical/visual baseline: [Guardian R2 f5facb1](https://github.com/jaychtw/armorheart/tree/f5facb1d7264e328c30b778c31b4a4cce3c64999). Planning branch starts at b4bf8ca, which descends from R2 and includes the owner's acceptance record. Current remote main and R2 tips remain a70a447 and f5facb1 respectively.

Governing [GDD v1.0](../ARMORHEART_GDD_v1.0.md), [UGDS 1.0.0 pinned d5c6696](https://github.com/jaychtw/game-development-standards/blob/d5c6696efdd6efc028118600466db44aecae0c9b/UGDS.md), [adopted AICP 1.2.1 pinned b8b9de0](https://github.com/jaychtw/game-development-standards/blob/b8b9de0d4faaf666fb53cec83ff8516bccf5bd5b/AI-COLLABORATION-PROTOCOL.md). Local copies read. Current shared README and AICP changes at [a0f9183, version 1.5.0](https://github.com/jaychtw/game-development-standards/tree/a0f91837f170da97b98afe979afb473f169edf58) were reviewed as supplementary guidance on proportionate work and recovery, not adopted or substituted for this project's pins. The older QA's pending visual-acceptance text is historical; updated PROJECT_STATE and owner acceptance supersede that status, not its evidence limitations.

**Feasible as one small, static-browser mission without new runtime dependencies.** Primary risk is map/geometry and phone readability, not shortest-path cost. Approval should include the explicit map-block-size proposal below. This is a bounded teaching scenario, not a claim of final campaign difficulty. No Level 1 runtime code, assets or controls have been changed in this assessment. Historical R2 reports were inspected; their 24/27/81 passes were not rerun for this Offer.

## Concrete map: fork, then offset exit gate

World and square camera remain 768x768. Active portrait rectangle: x=192..576, y=0..768 (384x768). Side bands are unplayable military scenery with visibly continuous, indestructible boundaries at x=192 and 576; tank and crowd obey these same boundaries, projectiles cannot pass around them. They are collision bounds, not destructible tiles. No camera zoom or tank scale change proposed.

**New mission map unit: 128x128 world units per single logical wall block**, each destructible block still exactly 1 HP/one shell. R2 range keeps its 64-unit blocks. This is an explicit new-map geometry/design proposal, not an already-approved change. It avoids creating 64-unit holes for the accepted 93x57.5 hull. Do not silently group four independently visible bricks into a one-hit object: draw each 128-unit block as one coherent brick mass using the accepted material style, with matching collision and navigation bounds. Tank scale .5, speed 156, muzzle reach 68, shell speed 480 and 1-second cadence stay unchanged.

Each symbol below is 128 units; y increases downward. Columns A/B/C start at x=192/320/448. Rows 0..5 start at y=0/128/256/384/512/640. Map notation is planning, not runtime data.

```text
       A     B     C
 r0    .     E     .    north refuge / exit
 r1    S     U     S    upper gate, y128..256
 r2    .     .     .    turning chamber, y256..384
 r3    L     S     R    choose left or right opening, y384..512
 r4    .     .     .    staging area
 r5    .    T/C    .    south start

 S = permanent steel; L/R/U = one-hit brick blocks
 E = exit zone; T = Guardian; C = one logical crowd
 . = traversable ground, not a required demolition target
```

| Object | Bounds / initial state |
|---|---|
| Upper-left steel | x192..320, y128..256 |
| Upper gate U (brick) | x320..448, y128..256 |
| Upper-right steel | x448..576, y128..256 |
| Lower gate L (brick) | x192..320, y384..512 |
| Lower-center steel | x320..448, y384..512 |
| Lower gate R (brick) | x448..576, y384..512 |
| Tank | center (384,672), facing up; accepted Guardian geometry |
| Crowd | center (384,704); one logical group, radius 16 envelope |
| Exit | x320..448, y0..96; full group containment required |

Initially both horizontal wall bands seal the corridor. Choice: open L **or** R, then U; opening the other lower gate is optional, never required by a destruction counter. Two effective shots are sufficient; one stationary firing line cannot solve the mission. From spawn, northbound shots hit permanent center steel. From either lower gate's firing lane, the upper band is steel; the tank must enter the chamber and realign toward U. No piercing or barrel-overlap bypass permitted.

Example left solution (right solution mirrors it):

1. Move west from(384,672) to(256,672), face up, shoot L.
2. Advance through its 128-wide opening to(256,320). The entire 93x57.5 hull fits, including a cardinal turn in the chamber.
3. Move east to(384,320), face up and shoot U. The muzzle may overlap the block; accepted first-obstacle sweep still consumes the shot at U.
4. The crowd now finds a complete route and leaves automatically; opening R is unnecessary. Tank need not reach the exit, escort physically or remain in front.

Analytical hull envelopes at these waypoint turns fit; this is not an actual renderer/input playthrough. All reachable positions, partial states, corners and corridor boundaries still need implementation-time contact tests. A center clearance correction exceeding R2's 19-unit test envelope is a map defect to resolve/return to Offer, not permission to change recoil, collision fidelity, speed or tank size.

### Planning connectivity check actually performed

A disposable, independent 32-unit-grid BFS calculation with16-unit crowd clearance examined all 8 subsets of the three bricks. It was assessment arithmetic, not a Level 1 module or gameplay test. Full route exists exactly when **U and at least one of L/R are removed**. No removals, U alone, either lower gate alone, or L+R without U remain blocked. With U+L, U+R or all three removed, shortest sampled start-to-exit route is 800 world units. Equal alternatives choose left under the proposed tie order. Full navigation/render correctness is not established by this calculation.

At proposed crowd speed 48 units/s,800 units take 16.67 seconds after a route opens. Tank waypoint travel is 608 units /156 =3.90 seconds, plus projectile travel, firing alignment and input overhead. These are idealized lower-bound estimates, not playtest completion times. A90-second deadline is generous for a two-shot teaching puzzle; urgency/difficulty must be judged by the human gate rather than claimed from arithmetic.

## One-group navigation and dot motion

Proposed pure module: a cardinal, uniform-cost graph with 32-unit spacing. Active node centers x224..544 and y32..736 on multiples of32; at most 253 candidates before blocking. No diagonal movement, corner cutting, individual pathfinding, collision avoidance or civilian steering.

A node and its connecting segment are legal only when the radius 16 group envelope stays inside the active rectangle and outside every live wall. Inflate wall rectangles by 16 when checking the center; exact contact is legal, interior penetration is not. Validate swept edges too, not just endpoint cells. Exit goal nodes have their entire envelope inside the exit rectangle (x352/384/416, y32/64 for this map). Tank and shells never enter the navigation occupancy grid; shots pass through the group without damage or consumption.

Reverse multi-source BFS from goal nodes computes shortest step distances after each wall-revision change. Choose neighbors in fixed **up, left, right, down** order among equally short continuations. Fixed goal ordering resolves any remaining equality; do not depend on object iteration or randomness. With both gates open, this gives the left route at the symmetric initial position. Same inputs/map revision produce the same route.

Initialize/rebuild on mission start, Retry and effective brick removal; batch multiple removals within one simulation update. Steel impacts do not change topology. No frame-by-frame replan when walls are unchanged. If a destruction occurs during an edge traversal, compare cost via both legal endpoints (remaining continuous distance plus BFS distance), choosing the shortest; equal cost prefers continuation, then fixed tie order. This avoids a teleport to a cell center, needless oscillation, or ignoring a newly shorter route. Only wall removal occurs in M1, so the existing edge cannot suddenly become blocked. Empty/no-route state means wait in place, not head toward the nearest blocked gate or walk through walls.

Render 12 decorative dots with fixed deterministic offsets whose centers lie within radius 12 and dot radii at most 3; all pixels remain inside the radius 16 group envelope. Translate them with the same group center along cardinal segments; no independent AI or free wandering. Optional tiny opacity/stride cue must stay within the envelope; disable nonessential motion under reduced motion. Do not spread a formation across a wall or leave a trailing dot outside the exit when awarding success. Add an outline/contrast treatment and a persistent localized status so the crowd is identifiable without relying on color or tiny dot animation.

The crowd waits at the starting area until a **complete exit route** exists, even after L or R opens. Advancing toward a blocked frontier would be a different rule; it is not proposed here. This follows the GDD's wait-if-no-route behavior and should be taught as “Open a complete route.”

## Timer, outcomes and minimum mission UI

- 90 seconds is a provisional active-play deadline. Start only on explicit **Start mission**, after map/assets/instructions are ready. Entry screens and loading consume no time.
- Track unpaused, visible monotonic elapsed time independently of R2's clamped `step()` time. A slow frame must not refill or extend the deadline. Use the same active-time interval for group advancement and event timing; process any crossed route nodes, not one node per frame. Pause/hidden-tab suspends the mission clock and clears input; resume rebases the clock with no catch-up penalty.
- Win only when the entire logical envelope first enters the exit at an active timestamp **strictly before 90.000s**. Exactly 90.000s is timeout; compare event times, not rounded HUD text or an arbitrary update-order race. A group arriving at 89.999s succeeds even if a render frame is late. Once terminal, freeze mission input, movement, timer and further wall effects.
- No enemies or normal tank damage in M1. Do not implement HP, immunity, death systems merely because later GDD stages need them. Timeout is the mission's failure. Bombers remain narrative copy/failure framing only; no bomber assets, attack simulation or destruction cinematic.
- Success: **Replay / Level exit**. Timeout: **Retry / Level exit**. Level exit returns to a minimal local scenario chooser (Guardian range / Breakthrough), not a campaign selector with locked or fake stages. Show paused confirmation before abandoning a running mission. Retry recreates the original map, group, clock, settings-preserving UI, shells/cooldown/events; no stale path or partial previous completion. No automatic Next-stage flow.
- Preserve saved language/mute/reduced-motion settings and storage fallback. Mission run/progress need not persist across reload in this independent POC; reload returns to entry. No account, save-game campaign, unlock or commendation system.

## Integration scope and sequence after authorization

Inspectably retain the R2 proving ground as the default scenario and its accepted assets/controls. Use a small scenario/mission adapter; do not replace the renderer or adopt a framework.

| Proposed location | Bounded purpose |
|---|---|
| `src/maps/breakthrough.mjs` (new) | Exact wall bounds, spawns, corridor and exit metadata; proposed map only after commitment |
| `src/navigation.mjs` (new) | Pure occupancy/edge validation, deterministic BFS and route distances |
| `src/breakthrough.mjs` (new) | One-group position/path revision, timer and mission state/outcomes |
| `src/engine.mjs` | Parameterize map/active bounds and rectangle wall dimensions, defaulting existing range walls to 64x64; preserve accepted tank/projectile behavior; scenario-specific completion policy replaces unconditional six-brick completion for M1 only |
| `src/app.mjs`, `src/i18n.mjs`, `index.html`, `style.css` | Scenario choice/mission HUD, group/exit rendering, bilingual instructions/results/exit confirmation; keep accepted tank draw/effects, keyboard/touch mapping, industrial style and focus behaviors |
| `tests/`, `tools/`, QA/evidence | Mission/navigation tests; real-input M1 evidence; preserve original R2 coverage; update preview bundling for the additional local ES modules and package reproducibly |

R2's `CELL` currently controls wall AABBs in multiple functions and the renderer assumes 64-unit wall faces. Generalize each of those consistently, rather than changing global CELL or scaling the whole world. Preserve default range initialization and its six-block completion. Current static preview bundler concatenates only engine/i18n/app; update it deliberately for new local modules and prove no extra runtime requests. No external bundler or package required.

After commitment: first deliver geometry/navigation and negative-rule tests, then mission state/UI integration, then actual browser/touch/evidence and human review. Use a dedicated implementation branch, meaningful safe intermediate/final GitHub pushes under adopted AICP §6.2, verify remote SHAs. Do not force-push, merge, deploy, alter Pages/settings or start another stage.

## Proposed acceptance criteria

All below are **future, not yet verified**:

1. **Map and accepted Guardian baseline:** specified boundaries, three brick/three steel blocks and spawns agree across drawing, physics and navigation. Both proposed solutions work with real input. All four facings, blocked turns, parallel sliding, corners and every brick-removal subset stay clear of walls/bounds without large turn relocation. One-hit/no-piercing rules, scale, speed, recoil, muzzle attachment and 1-second hold-fire remain unchanged. Preserve R2 range and rerun its 24 rule, 27 browser and 81 focused checks with honest new counts/failures.
2. **Navigation and negative paths:** independently compare shortest distances with an oracle on authored maps; all 8 brick subsets match the truth table above. Initially no route. Missing U remains blocked. Equal alternatives stable; destruction can select a genuinely shorter route from a moving center without jitter/teleport; steel impacts cause no replan. No diagonal corner cut or envelope/dot penetration. Tank overlap and player shots leave crowd state unchanged. Same input/map revisions replay deterministically.
3. **Mission boundary cases:** entry/loading/pause/hidden tab do not spend time; resume does not jump. Exercise long visible frames, timer below/at/above deadline, last-shot and arrival near deadline, center-only versus full-envelope exit, simultaneous topology/timeout events, immutable terminal result, repeated Retry and exit confirmation/cancel. Destroying all bricks or the tank reaching the exit alone does not win. Retry has no stale shells/path/deadline.
4. **Actual browser loop:** real keyboard and simultaneous touch complete left and right routes; hold stationary Fire at spawn never completes. Demonstrate waiting, opening one lower gate while crowd stays blocked, opening U/replanning, evacuation success, timeout, retry, exit and live language switch without clock reset. Include the running non-fixture map as well as isolated fixtures; snapshots may observe, not replace gameplay input.
5. **Presentation/accessibility:** actual EN/zh-TW captures at 320/390/768/1440 widths plus short landscape; focused four-direction contact and frozen-recoil evidence. Show obstacle readability, group/exit/status and timer during play, success and failure. Keep 44px touch targets, keyboard/focus and reduced motion/mute; automated accessibility plus manual text/canvas contrast review, with incomplete items disclosed. No new horizontal overflow, control overlap or regressions in scene visibility. Prove fully bundled preview functions with additional requests blocked.
6. **One human playtest gate:** at least one independent first-time player, ideally on an actual phone, can identify the crowd, goal and steel/brick distinction, discover one of the two routes and complete within 90s by the second attempt without spoken step-by-step instructions. Record device, language, attempts/time, confusion and feedback; owner judges whether selective repositioning and urgency are clear and satisfying. If no participant/device is available, mark this gate Not Verified and return for review, not fabricated acceptance. Owner explicitly accepts or redirects the M1 experience before any expansion.

No Level 1 test pass, balance result, rendered M1 screenshot or player approval is claimed now.

## Risks, defaults and commitment needed

| Issue | Proposed default / response |
|---|---|
| New 128-unit blocks vs range's 64 | Explicit Offer decision; one logical block/one hit and honest visible silhouette. If owner wants 64-unit individual blocks, return a revised map/clearance Offer rather than silently introducing narrow gates or tank shrinking |
| Phone scale | On the existing 278–343 CSS-pixel square, active corridor is roughly139–171px wide, blocks 46–57px; tank hull roughly34–42px long/21–26px thick; group envelope12–14px across, individual dots around2px. Outline/status required; actual readability unverified. Do not enlarge the tank/zoom/crop accepted scene without approval |
| Fitting field and controls | Existing range requires scrolling on short phones/landscape. M1 may collapse the inspection sidebar into a closed details section, leaving accepted art/controls unchanged; budget the mission HUD and primary controls in the portrait viewport. If this needs a substantial layout redesign or cannot be usable at 320px, escalate with actual captures; do not call full-page screenshots single-screen proof |
| Puzzle too easy /90s too generous | Two-shot choice is intentional for M1. Analytical ideal completion ~22s does not prove urgency or first-time difficulty. Keep 90s for first playtest; propose tuning only with evidence, no automatic harder map, timer reduction or extra shooting checklist |
| Large-wall barrel/shooting integration | Preserve first-obstacle sweep from tank center through muzzle and shell travel; verify near-wall overlaps and consumed shots against 128-unit rectangles |
| Crowd routing clarity | No partial-frontier motion; explicit waiting status, non-color-only group/exit markings. 12 dots are one group, not 12 independently arriving civilians |
| Accessibility and legal limits | Do not claim full screen-reader spatial play, physical-device coverage or production license. No paid art, APIs, telemetry, runtime network assets, bomber simulation or copyrighted backgrounds |

Engineering defaults (BFS, 32-unit navigation, 12 dots, 48 units/s, deterministic tie order, timeout precedence and pause behavior) can be accepted with the Offer rather than sent back as separate routine questions. No proposed waiver of UGDS; full campaign systems are excluded by this bounded assignment, not marked complete.

**Requested next commitment:** authorize implementation of this bounded M1 Offer, including the 128-unit single-hit wall map, one non-blocking crowd, provisional 90-second timing and the stated UI/test/human-review scope, on a dedicated development branch with safe checkpoint pushes. Preserve R2 Guardian assets/mechanics and the original range. Budget remains $0. No other tanks, enemies/bosses, campaign progression/unlocks, new art-production program, merge, release, public deployment, publication or standards-pin changes. Material geometry, quality or timing discoveries return for a scoped counteroffer. Stop at M1 Confirm & Close.

## Preservation and verification of this Offer

Only planning Markdown and a project-state pointer are changed. Current pre-push read-only checks: no Actions workflows/rulesets, Pages remains workflow-based/main source; no active local Git hooks. Webhook/secret metadata 403 remains unverified; no secret values requested or included, no settings changed. Planning branch only, no force push. Recheck remote tip before preserving and verify exact SHA after push. Existing R2 assets/runtime/preview must remain byte-identical to the accepted baseline in this planning branch.
