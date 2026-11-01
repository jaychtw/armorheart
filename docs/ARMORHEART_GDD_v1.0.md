# Armorheart — Game Design Document v1.0

**Status:** Owner-approved design baseline for feasibility assessment; NOT an implementation/release authorization.  
**Date:** 2026-11-01 (Asia/Taipei)  
**Owner:** Human creative director  
**Project repository:** Not yet identified/created; proposed `jaychtw/armorheart` (not confirmed).  
**Game standard:** UGDS v1.0.0, immutable tag `v1.0.0`, commit `d5c6696efdd6efc028118600466db44aecae0c9b`.  
**Collaboration:** AICP v1.2.1, reviewed at standards commit `b8b9de0d4faaf666fb53cec83ff8516bccf5bd5b` (pin if adopted in repository).  
**Budget:** $0 incremental cost.  
**Deployment:** Not authorized.

## 1. Pitch and design pillars
A top-down, four-directional arcade tank action-puzzle game. A lone tank opens evacuation routes and defeats three distinctive high-value targets. Inspired by the accessibility of classic tank arcade games, not a remake of any copyrighted work.

1. **Destruction with purpose:** Shoot obstacles to alter usable routes or cover; mission objectives, not destruction count, determine success.
2. **Arcade clarity:** Deterministic one-hit walls; no physical fragmentation simulation; satisfy impacts with sparks, dust, recoil, flashing, sounds, and modest shake.
3. **Distinct encounters:** Evacuation, jumping monster, moving battleship, static heavy fortress.
4. **The tank is the hero:** Strong recognizable silhouette at true play scale; high detail goes to tank and bosses, while level geometry is simple.
5. **Fair failure and replay:** Three tank HP, clear visual telegraphs, fast level retry, all levels selectable.

## 2. Governing baseline and interpretation
UGDS requirements apply unless a documented owner-approved exception is necessary. Bilingual English/Traditional Chinese live UI, desktop and touch operation, responsive layouts, accessibility and quality gates remain required. The numerical values below are **initial implementation values approved for testing**, not irrevocable balance outcomes. Changes affecting experience return for owner review. Codex must independently retrieve and read the immutable UGDS and adopted AICP before implementation.

**Decision provenance:** Consolidated from owner decisions in the current conversation. Visuals and exact tank designs remain subject to a separate owner art approval; the existing tank prototype pack is experimental, not an accepted production asset set.

## 3. Movement, shooting and collision
- One player-controlled tank; four cardinal directions only. Pressing a direction **immediately changes facing**, even if movement is blocked; continued input moves in that direction when possible. Turret fixed to hull, pointing along facing direction.
- Fire immediately when ready. Holding Fire repeats at a **1.0-second cooldown**, with **unlimited ammunition**. Single shared shell type. No player turret-aim mechanic.
- All projectiles deal **exactly 1 damage** on one effective collision; no piercing. A projectile is consumed at the first wall or eligible entity hit, including a wall it destroys. Prevent repeated hits from one projectile. Collision with indestructible walls consumes the projectile without changing the wall.
- Tank HP = **3**. On effective damage, lose one HP and flash/become immune to **all defined damage** for **3 seconds**; can still move and fire. The hit reducing HP to zero destroys tank and produces failure/retry screen, returning to **the beginning of the current level** on Retry. No whole-campaign reset.
- Enemy projectiles damage the tank; Kong's physical contact deals one HP if not immune. Other environmental contacts are not presumed damaging unless specifically authorized later. Refugee dots are neither damaged by player fire nor obstruct tank movement.
- Wall types: **destructible 1 HP**, visually distinct **indestructible** world barriers. No two-hit fortified wall. Both block tank movement and projectiles; enemy fire also destroys destructible wall blocks. Destroyed wall blocks are immediately removed from the navigation/collision map. Minor temporary cosmetic particles are non-physical.
- Initial effects: muzzle flash, retracting cannon barrel, impact spark, flash, transient dust/debris, restrained shake and audio. Accessibility: reduced-motion behavior and audio mute.

## 4. HP and boss degradation
| Entity | Full HP | Active visual states | Defeat |
|---|---:|---|---|
| Tank | 3 | Flash/immunity following nonfatal hit | 0 = retry level |
| Destructible wall | 1 | Intact | 0 = removed |
| Kong | 4 | Intact (4), Fatigued (3–2), Wounded (1) | 0 |
| Battleship | 6 | Intact (6–5), Smoking (4–3), On fire (2–1) | 0 |
| Fortress | 8 | Intact (8–6), Broken (5–3), Half-destroyed (2–1) | 0 |

Boss HP thresholds are **proposed defaults accepted for initial testing**; visibly readable changes are mandatory. Behavioral shifts at each degradation stage are optional proposals requiring evidence and review, not hard requirements.

## 5. Four-level campaign
All four missions selectable from the start. Completion tracked independently for each mission. The former retreat/suppression mission was removed from v1.

### Level 1 — Breakthrough (evacuation)
- Shared overall square arena/viewport framework; play constrained to a **narrow central portrait corridor**. Non-play sides are scenery/boundaries.
- One logical refugee crowd rendered as multiple animated dots. No individual civilian AI. The crowd selects the **shortest traversable route** to the exit on the grid, recomputing after wall removal, with stable tie-breaking to avoid jitter. If blocked, it waits. It does not absorb shells or obstruct the tank. Crowd must never visually traverse a solid obstacle.
- Wall masses comprise one-shot destructible blocks interspersed with indestructible blocks, preventing a stationary player from simply firing a straight passage from start to exit. Allow meaningful routes and re-positioning; don't force a rote demolition checklist.
- **Win:** entire logical crowd reaches exit before deadline. **Fail:** countdown expires or tank loses all HP (though this stage presently has no enemies, so ordinary gameplay should not damage tank). **90 seconds** is a provisional playtest target. Bombers may provide a noncombat cinematic deadline/failure framing; no bomber combat.
- Initial layout and pathfinding should be validated for solvability, clarity, and an achievable time target.

### Level 2 — Colossus (Kong)
- Square or near-square arena. Kong follows a learnable jump sequence: upper-left → upper-right → lower-right → lower-left → center → repeat. At each landing pauses **2 seconds**, with visible looking-around/recovery and readable next landing telegraph. Exact jump transit time and collision boundaries are playtest values.
- Tank contacts Kong: one effective damage, governed by 3-second immunity. Kong may destroy destructible walls. Other attacks are unapproved until assessed.
- **Win:** Kong 0/4 HP. **Fail:** tank 0/3 HP. No arbitrary timer.

### Level 3 — Interception (battleship)
- Ship cruises along perimeter in inverted-U path: one side → top → opposite side → exit. Predictable route, with sufficient visibility/firing opportunities. Three spaced projectiles per volley fired **every 3 seconds** as an initial timing. Firing direction is horizontal inward on vertical side legs and vertical inward across top leg, not homing; exact targeting/orientation to be evaluated.
- **Win:** ship reaches 0/6 HP before exiting. **Fail:** ship exits alive or tank 0 HP. Speed, shell speed, size and duration must be playtested together.

### Level 4 — Siege (fortress)
- Static fortress with **five-projectile radial/fan volleys** every **3 seconds** initially. Volley direction may be aimed at tank position when fired, but projectiles do not home afterward. Gaps widen, allowing dodging. If volleys become unfair or too busy, consider waiting until previous shots leave the arena; submit revised offer rather than silently changing a material mechanic.
- Walls offer shielding but destructible walls can be destroyed by enemy shells. Include indestructible barriers where needed for reliable geography and fairness. Readable telegraphs/openings.
- **Win:** fortress 0/8 HP. **Fail:** tank 0 HP.

## 6. Tank art and collection
- Bird's-eye top-down presentation with selective 2.5D cues. Fixed turret; emphasize silhouette, barrel, hull geometry and visible tracks. Preserve signature identity; simplify vents, cables, tiny hatches and bolts invisible at gameplay scale.
- Experimental artwork: T-01 Guardian (A-1), T-02 Bulwark (C-1), T-03 Vanguard (E-1), T-04 Sentinel (S-1). Names and visuals provisional. A four-direction transparent sprite prototype pack exists for technical evaluation; 64px/128px candidates with larger masters. Do not call these production-ready or mistake presentation art for animation proof.
- **Four cosmetic-only tanks with identical statistics**, if production validation supports them. Start with T-01; every **distinct** mission first completed unlocks the next tank, irrespective of mission number (up to all four after three distinct clears). Fourth distinct clear awards campaign commendation. Preserve free level selection. Never gate a mission behind a tank unlock.
- Barrel recoil is desirable: short backward motion along barrel axis then recovery. Animations and at-scale quality must be verified in a genuine game renderer before scaling asset production.

## 7. UI, progress, accessibility
- Level-selection menu: all stages available, completion checkmarks, selected unlocked tank, visible English/Traditional Chinese language toggle, saved locally when storage permits.
- End-of-level: short congratulatory medal/commendation animation, clear mission achievement, optional tank unlock; options **Next / Level Select / Replay** as applicable. Failure: **Retry / Level Select**. No forced whole-campaign restart.
- Desktop arrow keys for four-direction movement; clear Fire mapping to be selected in implementation brief, hold-to-fire. Mobile controls are delegated to advisory AI/Codex to propose and empirically validate; should support simultaneous direction and firing, appropriate touch targets, and not obscure arena.
- Centralized EN/zh-TW resources and instant switching; meaningful state and settings persistence; graceful storage failure. Respect reduced-motion, contrast, keyboard focus and mute requirements.

## 8. Technology, performance and art gates
- Target: lightweight browser game, compatible with static GitHub Pages if feasible. Runtime framework, world-unit grid, final sprite dimensions, collision and animation approach remain open for Codex Offer.
- No accounts, paid services, telemetry or external production dependency without express approval.
- First risk-based evaluation should import the actual provided tank prototype sprites, test at rendered gameplay sizes, show four cardinal facings plus in-engine recoil and shooting, and assess transparent-edge quality, sprite framing, coherence, memory/render cost and touch layout. A concept sheet alone does not prove viability.

## 9. Acceptance / verification plan
- Deterministic rules tests: turn while blocked; immediate and held firing cooldown; one shell one collision one damage; destructible/indestructible walls; invulnerability all damage sources; tank death/retry; boss HP stage boundaries; local completion/unlock order and storage fallback.
- Browser playthrough: representative Level 1 path opening and crowd path recalculation; all boss movement/firing/death pathways; failures and replay; both languages; keyboard and touch-emulated inputs; phone/tablet/desktop viewports; accessibility scans and human visual review.
- Playtest tuning: Level 1 90-second feasibility, wall count/layout; boss flight/volleys and health; bullet speed and intervals; tank gameplay scale; animation/effects satisfaction.
- Explicitly distinguish local test success, Git push, CI, deployment, live gameplay verification, and human artistic acceptance.

## 10. Explicit exclusions and open evidence
**Out:** realistic rubble physics; penetration; multihit walls; conventional enemy-tank combat; former troop-withdrawal Level 2; unrestricted added ammunition/weapon systems; multiplayer; monetization; mandatory scoring/ranks.

**To verify via Codex Offer/POC:** project architecture, browser performance and visual target at gameplay scale; final four-tank production feasibility, boss art pipeline; map layout sizes and camera; mobile control specifics; projectile speeds/volley collisions; impact visual and sound quality; exact numeric tuning; legal/naming review before public release.

## 11. Change control and next gate
Owner has approved current recommendations as **initial design and testing defaults**, not proven balance or completed artwork. This GDD authorizes creating a feasibility **Offer**, not coding a game, pushing a release, merging or deploying. Any materially changed gameplay, expense, art target, external service or release scope returns for owner approval. After feasibility review, request explicit commitment for a bounded implementation. All development checkpoints follow adopted AICP §6.2 once authorized.
