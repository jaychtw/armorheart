# Breakthrough R3 — verified revised geometry

2026-11-03, Asia/Taipei. **Map assessment complete; geometry is ready for final R3 execution authorization for the stated provisional transport envelope. No R3 game or truck art has been implemented.**

The owner accepted the granular-cell, original transport, cardinal-pivot, deterministic routing and longer/lower-demolition versus shorter/higher-demolition direction, while rejecting the prior map. This bounded map revision supersedes the geometry in [c58a4cf](BREAKTHROUGH_R3_PROPOSAL.md). Guardian's engine/assets, world/scale, movement speed, immediate facing, recoil, controls, original proving ground and provisional 90-second deadline are unchanged. M1 remains the frozen runtime baseline [bfd2283](https://github.com/jaychtw/armorheart/tree/bfd228359fbf56f03f921cb3d3439c7c26ed5c79). Adopted GDD, UGDS 1.0.0 and AICP 1.2.1 pins unchanged.

## Revised map

[Coordinate/route diagram](../../planning/r3-geometry/map.png) · [vector diagram](../../planning/r3-geometry/map.svg) · [exact machine-readable map](../../planning/r3-geometry/map.json).

Keep 768x768 world and 384x768 active strip, x192..576/y0..768. **No larger playfield, tank shrink, delayed facing, invisible clearance gate, coupled cell deletion or engine correction cap is required.**

The layout is a compact S-bend/loop maze: a lower mixed 2x2 island divides approaches, a permanent offset spur obstructs the eastern lane, and an upper mixed 2x2 island requires turning into the refuge. The longer transport route crosses the strip twice and makes five quarter-turns; the shortcut cuts through the lower island and makes three. This is not two closed horizontal gates or a clear-all counter. Both routes preserve multiple surviving steel cells; the lower bricks can remain intact for the bypass.

Every listed obstacle is **one 64x64 cell**. Coordinates below are top-left origins; all have width=height=64. Cells use stable independent IDs; each brick is 1HP/one effective projectile and is removed alone. Steel is never removed. Cosmetic grouping creates no shared health or deletion. No object exists at omitted positions.

| ID | Kind | x | y | Bounds |
|---|---|---:|---:|---|
| U0 | Brick |320|128| x320..384, y128..192 |
| U1 | Brick |384|128| x384..448, y128..192 |
| US0 | Steel |320|192| x320..384, y192..256 |
| US1 | Steel |384|192| x384..448, y192..256 |
| P | Steel spur |480|256| x480..544, y256..320 |
| L0 | Brick |288|480| x288..352, y480..544 |
| LS0 | Steel |352|480| x352..416, y480..544 |
| L1 | Brick |288|544| x288..352, y544..608 |
| LS1 | Steel |352|544| x352..416, y544..608 |

Four destructible and five indestructible cells total. The lower island is offset by half a base cell horizontally/vertically relative to the upper one; the cells themselves remain 64 units. The spur is offset similarly. The 32-unit verge east of P is physically too narrow for either vehicle, not an invisible wall: Guardian's minimum hull thickness is 57.5, transport's body width56 plus navigation clearance. Draw real cell edges/verge clearly; never advertise it as a full vehicle lane. Other important passages are 96/128 units or larger. These offsets avoid the original64-unit enclosed notches and diagonal pinch points.

| Object | Proposed starting/goal geometry |
|---|---|
| Guardian | center (512,704), facing north/up |
| Transport | center (272,688), facing east |
| Refuge | x320..448, y0..192; truck must park wholly inside, facing north |
| Side/world bounds | x192/576 and y0/768, visible and impassable |

The refuge includes the initially blocked U0/U1 entrance region; paint its destination marking behind walls, with the visible refuge label north of them. Clearing a cell never expands the world or changes a vehicle hitbox. Full actual truck body/wheels/mirrors containment decides arrival; shadows excluded. The final verified goal body bounds are x324..380/y48..176, fully inside the refuge. The independent collision envelope is larger by4 on each side for navigation safety.

## Guardian verification — partial states and continuous clearance

[Actual engine checks](../../planning/r3-geometry/engine-results.json) · [continuous certificate](../../planning/r3-geometry/clearance-certificate.json).

1. Imported the **unchanged accepted engine**, asserting it is byte-identical to M1 before testing. No recreation of Guardian collision or a new approximation substituted for that engine. All 16 subsets of U0/U1/L0/L1 were checked, including single cells, asymmetric partial2x2 destruction and all cleared.
2. **530,944 actual-engine sampled turns passed** on an 8-unit spatial grid, all four initial/requested facings. Every accepted turn changes facing immediately and ends in a legal hull position. Worst sampled correction **15.5 units**. The original counterexample position(224,304), up→right, is explicitly replayed in the new layout and corrects 15.5 units, not 47.59.
3. The sample is strengthened by a **continuous configuration-space coverage certificate** over all legal center positions, including positions not reachable from spawn. For 16 states ×12 distinct facing transitions =192 cases, the checker partitions space using both old/new expanded wall and world faces. It includes all legal area cells, boundary segments and vertices. Each piece is covered by a closed legal target strip whose maximum corner-to-strip distance is<=19. **203,200 covered pieces, 0 failures; maximum certified bound 19 units**, numerical tolerance1e-7. The engine's 1e-8 contact tolerance is included.
4. Why this is a bound rather than more sampling: distance to one closed rectangle is convex, so its maximum on a rectangular source piece occurs at a corner. Proving every corner lies within 19 of a legal target strip bounds the whole piece. Axis-aligned expanded-obstacle faces delimit every possible legality change. The actual nearest-legal-position engine enumerates current coordinates and those true target faces, so it can choose a point no farther than this available legal point (apart from its negligible squared-distance tie tolerance). Its algorithm and speed remain unchanged.
5. Two deterministic Guardian movement/firing replays use actual `step()` and `canMove()` at every update. Long route: (512,704)→(512,400)→(288,400)→(288,160), face east and remove U0 then U1. Shortcut preparation: first move to(320,704), face up and remove L1 then L0; proceed through the cleared lower lane to(320,400), then use the same upper approach. Their maximum actual turn correction is 13.5 units. Shooting a chosen cell removes precisely that cell, leaving the other 2x2 cells/steel intact. Ten seconds of stationary Fire at spawn removes no brick.

The certificate proves the stated rectangle/axis-aligned physics geometry, not browser rendering, arbitrary future map edits or final art bounds. Hashes bind reports to the exact map and frozen engine. Any coordinate, cell, envelope or collision change must rerun it. Runtime and accepted assets are not modified by these assessment scripts.

## Transport clearance and route choices

[All 16 transport outcomes and action paths](../../planning/r3-geometry/transport-results.json).

Retain the accepted R3 direction: original U-1-inspired covered military truck with restrained W-1 camouflage, provisional **128x56 full visible body/wheels/mirrors**. Assessment uses 4-unit per-side clearance (136x64 padded rectangle), 48 units/s, 0.35s stationary 90-degree pivot, forward cardinal 16-unit steps and deterministic travel-time Dijkstra. This is a geometry tool only, not an integrated R3 planner or new game code.

Each translation checks the **entire swept padded rectangle**. Each pivot checks a radius76 disc against walls and world bounds, which contains the rotating padded rectangle: its actual circumscribed radius is 75.1531769 units. Closed contact is legal. Every recorded turn is also sampled at 1-degree increments for padded corner containment. Recorded routes have at least 4 units of extra turn-disc clearance from the nearest surviving wall/world boundary, beyond the already-padded vehicle. No point-path, diagonal cut, temporary clipping, forced truck displacement or visually false turn is used.

| Choice | Cells to remove | Travel | Quarter-turns | Predicted transport time after opening |
|---|---|---:|---:|---:|
| Longer bypass | U0,U1 only |976 units|5|22.083s |
| Shorter shortcut | U0,U1,L0,L1 |656 units|3|14.717s |

All 16 states were solved, not just these endpoints. A full route exists **iff U0 and U1 are removed**. With neither or only one upper cell removed, no complete route exists even if lower bricks are gone. Removing only one lower brick does not unlock the shortcut; its predicted time remains 22.083s. Both lower bricks are needed to shorten travel. Thus the extra two hits have a real physical purpose and are optional for victory.

Checked bypass turn/goal poses (heading after each turn): (448,688) north; (448,400) west; (288,400) north; (288,112) east; (352,112) north, fully parked. Starting heading is east at(272,688). Checked shortcut: (288,688) north; (288,112) east; (352,112) north. In-place turns have no translational jump. The maze visibly presents a bypass, a demolition island and a refuge approach, not a list of mandatory targets.

The shortcut saves 320 units and two pivots, approximately **7.367s of transport time**, at the cost of two additional one-second-cadence shots plus any player repositioning. This offers a meaningful preparation-versus-evacuation tradeoff. Keep 90 seconds; these analytical times exclude route discovery, aiming, player travel and the future truck presentation. They do not prove difficulty/fun or an independent player's completion time. Do not shorten the timer or add targets from these calculations alone.

## Updated bounded implementation scope after final authorization

The already accepted truck/granular/maze directions do not need reopening. The new geometry replaces the rejected candidate only. Next execution commitment should authorize this exact map plus:

- Map emits independent 64-unit cell entities; reuse existing rectangular wall helpers and nearest-first/non-piercing one-shot behavior. No Guardian mechanics, hull/anchors, scale, speed, facing, recoil, flash or range-map change.
- Author one editable original truck using U-1/W-1 only as conceptual reference; preserve provenance and verify actual visible silhouette against 128x56. Do not crop the reference sheet or call prototype rights cleared. If final artwork cannot fit the envelope at review quality, return a scoped art/geometry counteroffer and rerun clearance; never hide a larger body behind a smaller collider.
- Implement transport pose/action routing and oriented full-body exit using the proven envelope, while reusing M1's clock, pause, retry, localized waiting→evacuation cue, success/timeout and offline framework. No independent-unit refugee alternative, enemies, damage, fuel, pushing or next missions. Transport remains non-blocking/shot-immune as proposed; human review must assess large-vehicle overlap.
- Retain Guardian proving-ground regression coverage; reuse state-independent M1 clock/UI tests while labeling its old two-gate/dot fixtures as historical. Add granular destruction, all 16 map states, truck rotations/replanning/partial action pause/deadline/exit, real keyboard and simultaneous-touch mission loops, all-direction truck and preserved Guardian evidence, EN/zh-TW, 320/390/tablet/desktop layout/a11y and no-extra-network bundle checks.
- Safe dedicated implementation-branch checkpoints only; $0, no force push, merge, deployment/publication, standards-pin changes or unrelated scope. Stop at R3 creative-director Confirm & Close.

Geometry is now resolved **within current dimensions**; no material world-size or Guardian tradeoff is needed. Remaining gates are final execution authorization, actual truck-art bounds/quality, actual-render integration, phone readability, independent first-time-player/physical-phone testing and human judgment of the maze. This task did not generate truck art, run R3 browser gameplay or repeat M1's game suites. Those results are not fabricated from geometry tools.

## Reproduce and provenance

Assessment files are isolated under `planning/r3-geometry/`, never imported by the application or offline builder. From repository root:

```sh
python3 planning/r3-geometry/certify_clearance.py
node planning/r3-geometry/verify_engine.mjs
python3 planning/r3-geometry/verify_transport.py
python3 planning/r3-geometry/draw_map.py
```

The first three need only the existing Node/Python standard libraries. The optional diagram uses installed matplotlib; its output is a planning figure, not game art or a browser capture. `map.json` is the authoritative coordinate source; the JSON reports include map/engine hashes. Inspect old candidate and M1 via their immutable commits; do not retrofit historical acceptance claims. Other workspace planning drafts are preserved separately and are not the authority for this checkpoint. No existing runtime, tests, assets, preview or ZIP was edited.
