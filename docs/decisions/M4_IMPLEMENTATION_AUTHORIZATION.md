# Siege M4 — bounded implementation authorization

**2026-11-04 (Asia/Taipei).** The owner reviewed the [Siege M4 Offer](../offers/SIEGE_M4_OFFER.md) at `a44485475d573d65228d70e377e2561fed9f0e47` and explicitly approved proceeding. This authorizes **one bounded full playable M4 implementation cycle**, not merging, public deployment or release.

## Accepted creative scope

- Accept the proposed Fortress identity/silhouette and preliminary art direction as a working baseline. Finish material/lighting integration at real gameplay scale autonomously, retaining readable Intact (8–6), Broken (5–3), Half-destroyed (2–1) silhouettes. The initial vector study is not represented as final polished art.
- Accept the exact proposed 768×768 arena and map geometry: stationary `(256,64,256,160)` Fortress; two permanent central steel shelters, four individual destructible flank cells, northern static barriers, and Guardian spawn `(384,688)`. Preserve legitimate shelter/firing lines and fair tank movement.
- Accept **both tactics**: a fast ~10.44s modeled attack after repositioning that sacrifices two of Guardian's three HP, and a slower ~20.8–23.8s modeled attack/retreat sequence losing at most one HP. Their differing speed/survival tradeoff is intentional and **does not require forced continuous movement**. These are planning estimates, not completed actual gameplay results.
- Fortress remains **8 HP**, Guardian **3 HP** with **3s post-hit immunity**, five aimed but non-homing shots per eligible **3s** opportunity, **0.6s precharge** and three selectable visibly registered roof gun mouths. Shot spread, radius, velocity, collisions, cover erosion and same-frame chronology are per Offer; no timer, additional attacks, boss phase-based new abilities or HP changes.
- Preserve all accepted Guardian, Breakthrough R3, Colossus M2 and Interception M3 behavior and assets. Use bilingual EN/zh-TW, keyboard/simultaneous-touch, accessibility/reduced-motion/mute, local/offline build and $0 budget.

## Delivery expectations

1. Implement a selectable Siege Level 4, using native Canvas/ES modules and existing infrastructure; no engine rewrite.
2. Produce a visually coherent fortress and registered three-gun/five-shot effects, all three damage visuals, real-scale mobile/desktop evidence. Correct ordinary visual defects autonomously; escalate only material identity or gameplay conflicts.
3. Verify exact fan aim at launch (no homing), wall-vs-entity occlusion, independent one-hit bricks, indestructible steel, same-time impact ordering, tank immunity, victory/death/retry, pause/hidden, and all 16 cover-removal states.
4. Demonstrate actual keyboard and emulated-touch fast damage-trade wins and slower cover-based wins; report observed timing/HP and any fairness issues. Avoid silently tuning core mechanics or concealing safe/fast strategies.
5. Rerun focused and relevant earlier-stage regression checks; verify English/Traditional Chinese, 320/390/768/1440 layouts, focus/touch/accessibility, reproducible single-file offline playable ZIP with subsequent network blocked, clean build reconstruction and honest limitations.
6. Keep safe verified GitHub checkpoints, QA, screenshots/recordings, clear `PROJECT_STATE.md`, and finish at **Confirm & Close** for creative review.

## Boundaries

Authorized: implementation and proportionate correction of ordinary technical defects within the approved Offer. Escalate materially different mechanics, unfair/unplayable geometry or an unresolvable creative art conflict. Not authorized: tank roster/unlocks or campaign completion features, new mission, new attack types, unapproved paid service or dependencies, merges, deployment/publication, force-push, standards repinning or unrelated cleanup. Maintain known M3 original battleship-reference archival caveat rather than falsely claiming bytes were received.

The owner requested to proceed, so no additional creative approval question is needed before bounded implementation. This note supersedes the Offer's prior `not authorized` status while preserving its technical acceptance criteria.
