# Breakthrough R3 — granular maze and transport proposal

2026-11-03, Asia/Taipei. **Planning only; creative confirmation and a separate execution commitment required.** Source baseline [M1 bfd2283](https://github.com/jaychtw/armorheart/tree/bfd228359fbf56f03f921cb3d3439c7c26ed5c79). Owner requests granular cells, a readable maze and a single transport inspired by the supplied U-1/W-1 sheet; individual refugees remain a possible future alternative. This document proposes those changes; it does not record them as accepted or change gameplay/art.

**Conclusion:** reuse M1 rather than rebuild. Truck routing is feasible with explicit orientation/turn clearance. The candidate maze has analytically viable truck routes, but a concrete Guardian clearance problem below means it is **not an execution-ready approved layout**. Resolve that material experience issue before committing to final R3 implementation. M1's 51 rule/65 mission/27+81 range browser results remain historical evidence; none was rerun or relabeled as R3 acceptance here.

## What the inspected implementations actually provide

- Armorheart: rectangular wall dimensions, nearest-first one-shell consumption, bounds-aware Guardian collision, wall-revision-triggered navigation, independent active-time deadline, pause/retry/exit, bilingual mission HUD, localized route-open cue, offline module bundling and input/evidence tools. M1 represents each 128-unit block as one entity; removing one entity currently removes the whole block. Its navigation assumes a radius 16 group and position-only BFS; neither is a vehicle-clearance model.
- [Riot Defender main 50529a94d0ea5f97fdfe379c1bb1a4a6e497b28c](https://github.com/jaychtw/riot-defender/tree/50529a94d0ea5f97fdfe379c1bb1a4a6e497b28c): [simulation.js](https://github.com/jaychtw/riot-defender/blob/50529a94d0ea5f97fdfe379c1bb1a4a6e497b28c/src/simulation.js#L83) gives each unit its own position, speed, age and state. Blue units approach the center, stop at an actual closed-fence contact, then continue after admission. Red units wobble toward the center, follow the perimeter, reverse or retreat. Its analytic swept fence/gate contact is not maze pathfinding. [renderer.js](https://github.com/jaychtw/riot-defender/blob/50529a94d0ea5f97fdfe379c1bb1a4a6e497b28c/src/renderer.js#L43) deliberately separates a 10-unit visibility ring from a 5-unit collision core. No maze solver or physically sized truck is present to transplant. Source inspected, not executed; no Riot Defender files/settings/deployment changed.

For a later refugee option, reuse the **idea** of independent positions/state/speed and staggered arrival with swept wall checks. Each person would need valid maze routing and a defined last-person win condition. Do not import perimeter pursuit, enemy pressure, combat or decorative wobble that crosses walls. Do not build that alternative alongside the truck now.

## Candidate maze and granular destruction

Keep 768x768 world, 384x768 playable strip x192..576, unchanged Guardian scale/speed/controls and 90-second provisional deadline. Proposed base cell is64 units. Every B below is one independently identified 64x64, 1 HP destructible cell. S is an indestructible 64x64 cell. A 2x2 structure therefore contains four entities: one shot removes exactly one B, never its neighbors or the whole group. Keep visible cell seams; a shared cosmetic structure ID must not confer shared HP or deletion. Contact order and no-piercing stay as in the accepted engine. Do not count the18 occupied cells as a demolition checklist.

Columns0..5 begin at x192+64c. Rows0..11 begin at y64r. All unlisted cells are ground; side bands remain impassable scenery/bounds.

```text
       012345
 r00   ......   north refuge
 r01   ......   exit pad spans x256..512, y0..192
 r02   ......
 r03   SSSS..   permanent upper peninsula, eastern passage
 r04   BBBB..   four removable turn-pocket cells
 r05   ......   middle chamber
 r06   ......
 r07   ..SSBB   permanent center / optional eastern shortcut
 r08   ..SSBB   a2x2 steel block beside a2x2 brick block
 r09   ....BB   separate two-cell southern barrier
 r10   ......
 r11   ......   starting area
```

Exact cells: brick={(0..3,4),(4..5,7..9)} =10; steel={(0..3,3),(2..3,7..8)} =8. Tank spawn(256,704), up; proposed truck spawn(384,688), up. Tank spawn changes position only, not mechanics. The refuge is enlarged from M1's96-unit-deep exit because a128-unit-long truck cannot fit wholly in that pad. World/camera size remains unchanged. Both spawn and larger exit are explicit proposed design changes.

Two plausible solutions:

- **S-bend, four effective hits:** remove the four bricks in row4. Guardian can enter the left passage, reach the chamber and shoot their lower faces individually. The truck turns west in the staging area, drives north through the left passage, turns east in the newly widened chamber, then north through the upper-right passage. The entire eastern brick stack may remain intact.
- **Eastern shortcut, six effective hits:** clear columns4/5 in rows7/8/9, one cell per hit. Tank repositions between the two firing columns; repeated fire clears the nearest cell first. The truck uses the eastern passage directly. This costs two extra demolitions but less transport travel. Row4 bricks may remain intact.

This trades demolition effort against route length, with permanent geometry preventing one stationary line from solving the maze. Extra partial openings may be useful for firing or positioning; none is a truck route merely because a point can pass through. When both routes exist, select the shortest feasible predicted evacuation time. Never require clearing all 10 bricks. Difficulty and the90-second target need human playtesting; these are not balance claims.

### Concrete Guardian issue — do not hide it

A disposable assessment used the **unchanged M1 engine** on the candidate intact map and every single-brick removal, sampling positions at 8-unit spacing and all initial/requested facings. After removing brick(c0,r4), a valid up-facing tank at(224,304) turning right is corrected to(239.5,349): **47.59 world units**. No wall penetration occurs, but the jump is substantially larger than the 19-unit turn-clearance bound used to validate the accepted R2/M1 layouts.

The underlying incompatibility is real: a 64-unit opening can admit the Guardian's57.5-unit transverse hull, while its93-unit length cannot turn in that same opening/notch. Truck clearance does not fix it. Do not silently shrink the tank, enlarge/couple cell destruction, add invisible walls, gate player input, delay facing, alter its collider or introduce a new tank-turn mechanic.

**Recommended next boundary:** retain accepted Guardian behavior/quality, and return this candidate for a map-clearance counteroffer before final execution. A further map-only feasibility pass may rearrange cells without changing the selected maze/truck direction; it must demonstrate safe partial states rather than promise that more testing will fix this example. If the owner instead accepts the existing nearest-clear-position behavior with larger shifts in the R3 maze, record that explicit experience exception first. Changing Guardian mechanics would require separate authorization and is not recommended within this brief. This candidate is supplied for concrete review, not described as already satisfying the preserve requirement.

## Truck appearance and physical model

One original covered military transport, not a selection of truck variants. U-1 informs the olive cab, canvas-covered bed and recognizable utility silhouette; W-1 informs restrained camouflage/material breakup. Retain a clear cab/bonnet, three-axle wheel silhouette, canvas folds, controlled warm highlights and dark outline consistent with Guardian. No weapon/turret, passengers AI or damage states. Use the supplied sheet as concept only: do not crop a reference truck, import its background/shadows or treat the illustration as a licensed runtime asset. The attached image was visually inspected; the user's `/Users/...` path is not an accessible execution file. No claim of original-file byte/provenance inspection or production rights.

Proposed full visible body/wheels/mirrors envelope: **128 long x56 wide world units**, cab toward its heading; soft shadow may extend cosmetically. Add 4 units of navigation clearance on each side: effective 136x64 rectangle. These are design defaults, not measured bounds of a finished asset. After authoring an editable transparent SVG/layered master, measure its actual visible bounds/pivot and coordinate navigation with them; any necessary size change returns for review rather than hiding it in transparent padding or scaling the accepted tank. No truck asset is generated in this planning task. Do not deliver a generic flat placeholder as the promised visual quality.

At existing 278–343 CSS-pixel arenas, the visible truck would be about46–57px long and20–25px wide. This is more legible than the tiny synchronized dot group but needs actual 320/390px render review. Fine camouflage detail must remain subordinate to cab/bed/wheel recognition. Keep M1's localized waiting/evacuating status and route-open cue, adapted to “Transport”; explicitly identify the truck and destination without relying on color alone.

### Movement, turning and collision

- Proposed arcade motion: forward cardinal travel at 48 units/s; stop and pivot 90 degrees in 0.35s at a certified clear pose. No diagonal movement, realistic steering simulation, free reversing, sliding or pushing through walls. In-place truck pivoting is a **creative choice to confirm**, not an inferred physical capability from the reference.
- Position/heading state graph on a 16-unit lattice, four cardinal headings. At most 4,324 candidate poses in the strip before filtering. Validate each full oriented rectangle and its swept translation against **every surviving 64-unit cell and world boundary**. A64-unit point opening is not automatically a valid turn or long-body passage.
- For quarter-turn certification, use a conservative radius 76 swept disc around the pivot: the padded rectangle's circumscribed radius is 75.13. Test disc-vs-rectangle distance and bounds, not an unrotated endpoint box or point center. This may reject some physically possible tight turns; author 192-unit turn bays instead of silently squeezing the art. Later exact swept-rectangle optimization is unnecessary unless this conservatism blocks the agreed map.
- Use deterministic Dijkstra over forward and left/right turn actions, cost distance/48 plus 0.35 per quarter-turn. Unequal action costs make position-only BFS unsuitable. Stable action/node ordering resolves equal costs, preferring continuation, then left/right in fixed order. Objective is shortest feasible **predicted travel time including turns**; this differs from simply shortest centerline distance and should be confirmed with the design.
- Rebuild on effective cell deletion; steel impacts do not dirty topology. Finish a currently safe 16-unit translation/quarter-turn before adopting a new plan, then recompute from its exact legal pose. Maximum deferred translation is 0.333s; turns 0.35s. Removal cannot invalidate the current action. No teleport, jitter or free mid-edge reversal. Wait if no complete goal route exists; never advance to a blocked frontier.
- Keep the transport non-blocking to Guardian and immune to player shots, as M1's evacuees were. No tank/truck collision, fuel, repair, HP or escort distance. Large-vehicle visual overlap is a tradeoff for review; do not silently add traffic/avoidance rules. Truck cannot destroy steel or bricks itself.
- Success requires the **entire actual body/wheels/mirrors rectangle**, not its center/cab, inside the marked refuge, with northward final orientation. Shadow excluded. Destination poses are physically tested; continuous arrival time strictly before 90s wins. Preserve pause/partial-turn state, timeout precedence and terminal freeze; exactly 90s loses. A rear corner still outside cannot count as evacuated.

### Truck-only planning evidence, not gameplay verification

A disposable oriented-state Dijkstra calculation with the above body/margin/disc, 16-unit steps, 48 units/s and 0.35s turns found:

| Cells removed | Result from proposed spawn |
|---|---|
| None | No complete truck route |
| Only(c1,r4) | No complete truck route |
| Four row4 bricks |848 world units, 4 quarter-turns, 19.067s to a fully contained north-facing goal node |
| Six eastern shortcut bricks |656 units, 2 quarter-turns, 14.367s |
| All bricks | Chooses the same eastern shortcut |

The checked S-bend turn poses are(384,688):N→W,(288,688):W→N,(288,336):N→E,(480,336):E→N, then goal(480,128):N. The shortcut can move north to(384,656), turn east, travel to(480,656), turn north, and reach(480,128). Positions are design arithmetic, not actual browser captures. Times exclude the player's route-clearing time and do not prove fun, physical-device performance, or Guardian feasibility. The negative result for a one-cell opening helps prevent a point-path false positive.

## Bounded adaptation after confirmation

Reuse `engine.mjs` without changing Guardian mechanics: R3 map emits distinct 64-unit wall entities so existing first-hit damage naturally removes one cell. Keep global wall dimension helpers and original range defaults. Add an independent truck pose/turn planner alongside or parameterized from `navigation.mjs`; do not disguise a rectangle as M1's radius 16 crowd. Adapt `breakthrough.mjs` to the truck action sequence and oriented exit envelope while retaining its active clock/outcome/retry policy. Keep old M1 source/ZIP/evidence recoverable at its commit; R3 replaces the Breakthrough scenario, not the original Guardian proving ground. No third mission/menu proliferation required.

After geometry is resolved, author one original truck and provenance record, then reuse Canvas compositing, bilingual HUD, input, static bundle and evidence tools. Preserve range regression coverage; reuse state-independent M1 timer/UI tests, but label old two-gate/group-specific fixtures as legacy and add R3-specific expectations. Do not claim old 51/65 pass counts prove the new maze or truck.

Required future evidence: per-cell first-hit/non-piercing and mixed 2x2 integrity; all 10 brick subsets (1,024 combinations) for topology/pose feasibility; no full route initially; both selected demolition solutions and stationary-fire negative; oriented collision and swept-turn/long-frame boundaries; tank partial-state clearance counterexample eliminated or explicitly accepted; continuous replan and pause mid-turn; full rear/body exit at/before/after deadline; actual keyboard and simultaneous-touch route opening/evacuation/retry in both languages; 320/390/tablet/desktop captures with truck all facings and turns; preserved range rules/browser/recoil evidence; no extra-network offline build; accessibility audits/manual canvas review and an honest independent first-time-player gate. Physical-phone and independent-player tests are not performed by this design assessment.

No new framework, paid resource, network dependency, other tank, enemies, crowd alternative, next mission, production-art approval, standards-pin change, merge or deployment. Original M1 technical evidence remains historical and its human acceptance is not inferred. Budget $0. Safe development checkpoints only.

## Decisions and next authorized action

Creative confirmation should cover: **truck replacing the group**, U-1/W-1 original-art direction and approximate 128x56 body, arcade pivoting/clearance and non-blocking behavior, the maze's four-shot bend versus six-shot shortcut, enlarged refuge, and travel-time route objective. Separately resolve the **47.59-unit Guardian turn-correction issue**: recommended preserve the accepted quality bound and revise map feasibility before final R3 execution; alternatively explicitly accept the larger existing correction. Do not interpret approval of the truck reference as approval of that tank experience.

The earlier GDD and M1 authorization specify one logical refugee group and 128-unit one-hit blocks. This proposal intentionally changes that mission design to one truck and 64-unit cell damage; owner confirmation must be recorded as the scoped superseding decision. It does not revise the standards or authorize any subsequent campaign work. Current task authorizes inspection/proposal and safe preservation, not implementation. Next step is owner/advisory review of these choices, then a precise bounded commitment (or map counteroffer), not automatic coding.

Planning safety: clean baseline and current remote M1/main tips verified; no Actions workflows/rulesets, workflow-based Pages/main unchanged. Hook/secret metadata 403 remains unverified; no credentials read or saved. Only planning Markdown/project-state pointer changed. Runtime, assets, tests, previews and ZIPs must remain byte-identical to M1 in this branch. No published R3 or new game-test passes claimed.
