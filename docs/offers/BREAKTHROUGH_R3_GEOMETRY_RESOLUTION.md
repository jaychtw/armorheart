# Breakthrough R3 — verified geometry resolution

2026-11-03 (Asia/Taipei). **Geometry assessment complete; revised map ready for final execution authorization for the stated provisional vehicle envelopes. No R3 game implementation or truck artwork added.**

Owner accepted the R3 truck, granular-cell, pivoting/routing and route-choice directions, but rejected the prior maze's 47.59-unit Guardian correction. This bounded revision supersedes **the candidate map** in [c58a4cf](BREAKTHROUGH_R3_PROPOSAL.md), not the accepted Guardian behavior. Source remains [M1 bfd2283](https://github.com/jaychtw/armorheart/tree/bfd228359fbf56f03f921cb3d3439c7c26ed5c79), with pinned GDD/UGDS/AICP unchanged. Assessment scripts import the actual unchanged engine. No framework, runtime navigation, renderer, controls, assets, preview, timer or ZIP was modified.

## Resolved map

[Exact machine-readable map](../geometry/r3/map.json) · [coordinate/route diagram](../geometry/r3/map-diagram.png) · [vector diagram](../geometry/r3/map-diagram.svg).

Keep the 768-square world and existing 384-wide portrait strip, x192..576, y0..768. Each cell is 64x64. The arrangement is a **compact loop maze**: a lower arrival funnel, central demolition island with flanking lanes, an eastern bypass with four turns and a through-island shortcut. It has no pair of full-width sequential gates or prescribed demolition counter. Open ground remains open; no invisible clearance gates are introduced for the Guardian. The vehicle-aware planner determines what the truck can actually turn through.

```text
         columns 012345   x =192+64*c
 row00           SS..SS
 row01           SS..SS
 row02           SS....
 row03           ......
 row04           ......
 row05           ..AB..
 row06           ..CD..
 row07           ......
 row08           ......
 row09           SS..SS
 row10           SS..SS
 row11           SS..SS   y =64*r

 S = permanent steel cell; A–D = independent one-hit brick cells
 . = road / turning bay, never an implicit obstacle
```

| Object | Exact bounds, units |
|---|---|
| Brick A, id0 | x320..384, y320..384 |
| Brick B, id1 | x384..448, y320..384 |
| Brick C, id2 | x320..384, y384..448 |
| Brick D, id3 | x384..448, y384..448 |
| Northwest steel block | x192..320, y0..192; subdivided into six 64-unit cells |
| Northeast steel block | x448..576, y0..128; four cells |
| Southwest steel block | x192..320, y576..768; six cells |
| Southeast steel block | x448..576, y576..768; six cells |
| Guardian spawn | (416,704), up |
| Truck spawn | (352,688), north |
| Exit marking | x352..448, y0..192;96x192 |

There are **four destructible cells and 22 steel cells**. A–D form one 2x2 structure but have separate IDs/HP: a shot consumes itself at the nearest wall and deletes **one** brick cell; steel is unchanged. Structure adjacency is cosmetic, never shared damage. Tank hull/barrel rules are unchanged. The centrally isolated island keeps 128 units of lateral space and 128-unit separations from the permanent blocks, eliminating the prior deep boundary notch.

Spawns are separate at their actual bounds, and the exit is long enough to contain the 128-unit body. The 96-unit exit width avoids a pixel-tight parking target; routing, not the player, handles alignment. These coordinate changes were authorized as part of map resolution; no active-strip/world enlargement, tank resizing or speed change was needed.

## Choices, physical routes and player access

The graph has no complete truck route initially or after any single hit. C+D opens the longer bypass. B+C+D opens a shorter through route while leaving A intact. All four bricks need not be removed.

| Choice | Cells removed | Truck distance | 90-degree pivots | Predicted truck travel |
|---|---|---:|---:|---:|
| Lower demolition / eastern loop | C,D |752 |4 |17.067s |
| Direct eastern-column shortcut | B,C,D |624 |2 |13.700s |
| Alternative northern cut | A,B,C |592 |2 |13.033s |

These are shortest feasible **travel-time** routes from spawn for the respective wall states, including 0.35s per pivot at 48 units/s. The two-hit optimum is slower than the three-hit optimum; this is not an artificial comparison against a deliberately bad two-hit route.

Certified main truck poses (heading0=N,1=E,2=S,3=W):

- **C+D bypass:** (352,688,N) → (352,464,N) pivotE → (480,464,E) pivotN → (480,208,N) pivotW → (416,208,W) pivotN → (416,128,N), fully in the exit.
- **B+C+D shortcut:** (352,688,N) → (352,464,N) pivotE → (416,464,E) pivotN → (416,128,N), fully in the exit.

The unchanged Guardian engine executed both demolition witnesses from its own spawn:

1. Move up to(416,500), fire north to remove D.
2. For the shortcut, fire north again after the normal cooldown to remove B behind D; each shell still destroys only one cell.
3. Move left to(352,500), face north and fire to remove C.

The two-hit witness takes 2.335 simulated engine seconds; the three-hit witness 3.335s, with exactly 2/3 shots and no other deletion. The engine also drives the Guardian, without further demolition, along every action of both truck routes after a clear-lane rejoin. These are assessment input sequences, not browser/human playthroughs.

## Verification across partial destruction

[Guardian report](../geometry/r3/guardian-results.json) · [transport report](../geometry/r3/transport-results.json) · [continuous clearance certificate](../geometry/r3/continuous-certificate.json). Both reports identify the map hash; the Guardian report identifies the exact imported engine hash.

**Guardian:** all 16 subsets, all four initial/requested facings, uniform 8-unit positions plus wall/world/hull critical-contact coordinates, tiny offsets on both sides and interval midpoints. This includes legal poses outside the selected witness paths. **3,086,432 turns checked; zero unresolved penetration or facing failures; maximum correction 19.0 units.** The verification ceiling was not relaxed. The actual engine, anchors, scale, speed and recoil remain unchanged.

The assay still catches the rejected map: its old pose(224,304,up) after the old boundary-cell removal turns right to(239.5,349), correction 47.5946. The same pose in the revised map turns to(239.5,304), correction 15.5. That negative control demonstrates the checker did not pass by weakening the rule or changing the engine.

The finite engine tests are complemented by a **continuous configuration-space certificate**: 16 masks x12 nontrivial facing pairs =192 cases. The verifier covers every legal source rectangle, contact segment and vertex with closed legal target rectangles, recursively subdividing until the maximum corner-distance bound is<=19. It certified 149,292 pieces with no unresolved region and maximum bound 19.0. The accepted turn solver enumerates obstacle/world faces plus the original coordinates, so it includes the nearest legal projection/corner; existence of a legal position within that bound limits its chosen correction. This covers the spaces between samples, rather than assuming a dense grid is a proof. It is a reproducible floating-point certificate (engine epsilon 1e-8, numeric tolerance 1e-7), not a proof-assistant or interval-arithmetic certification. Subsequent integration must still confirm rendered artwork/real inputs.

**Truck:** all 16 subsets on the complete finite 16-unit oriented lattice, with 128x56 actual body, 4-unit navigation margin per side (136x64 padded rectangle) and a conservative radius 76 swept-turn disc. The padded rectangle's circumscribed radius 75.13 is inside that disc. Each translation checks the full continuous swept box; each pivot checks disc-to-wall/bounds distance, not just its endpoint poses. Exact integer costs (20 ticks per 16-unit step, 21 per quarter-turn, 60Hz) give deterministic travel-time comparisons without floating tie ambiguity.

For both main routes, the turn disc has at least 4 additional units of clearance; body translation retains its specified navigation margin. A 64-unit opening can pass the 56-unit truck straight with 4 units per side, but does not thereby become a turn bay. North-facing success poses require the entire actual body/wheels/mirrors rectangle inside the exit; soft shadow excluded.

Complete state results, where a label means its cell is removed:

| Removed cells | Truck route |
|---|---|
| none; A; B; C; D | none |
| AB; AC; AD; BC; BD | none |
| CD | bypass, 17.067s |
| ABC | northern cut, 13.033s |
| ABD | none |
| ACD | bypass, 17.067s |
| BCD | direct cut, 13.700s |
| ABCD | northern cut, 13.033s |

All 32 one-cell-removal transitions were checked: existing legal poses, goals and **45,488 checked action-edge instances** remain legal as walls disappear. Thus a truck may finish a safe current translation/pivot before adopting a newly shorter route; destruction cannot invalidate that action or strand an already viable route. An existing valid route is never traded for a point-path false positive.

## Updated bounded implementation scope

After final authorization, replace only the Breakthrough map/transport presentation and its mission-specific planning adapter:

- Use the exact 64-unit cell entities above; retain engine first-hit damage, Guardian mechanics and original proving ground.
- Author one original U-1-inspired truck with restrained W-1 camouflage and an editable transparent source. Keep all body/wheels/mirrors inside the verified 128x56 envelope; measure actual pivots/opaque bounds before integrating. If artwork exceeds it, revalidate geometry rather than shrinking Guardian or hiding collisions.
- Integrate the verified forward/cardinal/pivot model and deterministic travel-time routing; keep the transport non-blocking to Guardian and unaffected by shells, as proposed. No reverse-driving, enemy AI, vehicle combat, individual refugees or realistic steering simulation.
- Retain 90-second deadline, exact before/at/after deadline handling, pause/mid-pivot state, retry, exit, bilingual HUD, route-opening cue, accessibility, touch/keyboard and fully bundled static operation.
- Give the player a readable explanation that the truck needs **turning room**, not merely a point-width route. Retain visible cell seams and an identifiable truck/exit; validate this on 320/390px screens. The loop/shortcut geometry must be visually taught rather than concealed behind invisible route costs.
- Preserve the geometry assays, range regressions and state-independent M1 clock/UI tests; add actual-render cardinal truck/turn/exit checks and full keyboard/touch playthroughs. Old M1 two-gate/group tests remain historical fixtures, not proof of R3 acceptance.

The approved 90 seconds is unchanged. Geometry-only estimates put the two main engine-clearing plus transport timelines near 19.4s and 17.0s, excluding human route discovery, input delays, concurrent timing details and game integration. The extra shot buys about 3.37s less transport travel. This supports a gentle teaching maze, not a claim that 90 seconds is balanced. No timer shortening or mandatory demolition additions are proposed without playtest evidence and further approval.

Remaining risks are **actual truck-art bounds, phone readability, communication of turning room, final visual maze acceptance and human balance/ergonomics**. Physical-phone and independent first-time-player tests have not been performed. The map is a compact loop-and-chord maze with a four-turn bypass, not an extensive labyrinth; the owner should judge its visual character from the schematic and then the implementation evidence. No expense, public deployment/publication, merge, standards upgrade or later mission is authorized.

## Reproduce / preservation

Assessment-only files, not gameplay code:

```sh
python3 tools/assessment/r3_transport.py
node tools/assessment/r3_guardian.mjs
python3 tools/assessment/r3_continuous.py
python3 tools/assessment/r3_diagram.py
```

Run in that order from repository root; the Guardian route replay reads the truck report. Python stdlib and Node run the geometry checks. The optional schematic uses already available Matplotlib; it is a coordinate diagram, not truck artwork or a game screenshot. No new dependency installation was required. Runtime/assets/tests/preview/ZIPs remain byte-identical to M1.

**Next gate:** final execution authorization for this resolved map and the previously accepted R3 direction. Geometry resolution itself does not authorize full R3 implementation. Preserve the accepted Guardian quality target, not the rejected 47.59-unit correction. Safe planning checkpoint only, no force-push or changes to main/M1/R2.
