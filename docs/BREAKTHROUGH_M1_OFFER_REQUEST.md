# Armorheart — Breakthrough Level 1: bounded implementation Offer request

**Status:** Owner authorized **feasibility assessment and scoped Offer only** on 2026-11-03. Not authorization to implement Level 1, merge, release or deploy.

## Verified baseline and authority

- Guardian R2 owner-accepted development baseline: `f5facb1d7264e328c30b778c31b4a4cce3c64999` on `dev/guardian-review-r2`; owner accepted collision, turns, muzzle flash, theme and frozen recoil.
- Follow project-pinned GDD and UGDS; review the adopted AICP and relevant current shared guidance. Do not silently change pins or retrofit the project.
- Read `PROJECT_STATE.md`, latest QA report, gameplay source, the GDD and acceptance evidence before offering an approach.
- Preserve the accepted Guardian mechanism and art baseline; no production-license clearance implied.

## Intended user experience — Breakthrough

A tank opens a safe passage for a small refugee crowd by selectively destroying one-hit walls and repositioning to shoot around permanent barriers. The crowd advances autonomously by shortest valid route whenever one exists; the player feels the urgency of clearing a corridor before the deadline. The **tactical arrangement**, not raw shooting volume or cinematic realism, is the puzzle.

**Candidate mechanics from the GDD (playtest-adjustable):**
- The overall arena framework remains square; Level 1 restricts active play to a tall central rectangle.
- Destructible one-hit blocks intermixed with distinctly rendered indestructible walls. A single straight-line shot from spawn must **not** solve the puzzle.
- No enemies. Bombers appear only as the narrative reason and eventual failure treatment, not as active threats in this milestone.
- Refugees display as several moving dots but are **one logical non-blocking crowd** (no individual pathfinding), unaffected by tank shots.
- Crowd computes shortest valid route to the exit, recalculating when wall destruction changes connectivity, and waits if none exists. Clarify tie-breaking, motion and passability at gameplay scale.
- Provisional **90-second** timer; win when entire logical crowd reaches the exit before expiration, lose on timeout.
- Preserve Guardian movement, collision, recoil, firing and effects already accepted, plus EN/繁體中文, keyboard/touch, responsive/reduced-motion behavior.
- Mission-specific failure, retry and level-exit affordances; no campaign systems beyond the minimum required by an independent Level 1 POC.

## What to assess and return (do not implement yet)

1. Inspect actual R2 architecture, geometry, controls, state handling and map layout; propose a Level 1 integration approach with minimal regression risk.
2. Propose a **concrete playable map** (coordinates or diagram) showing tank spawn, obstacles, initial impassable route, necessary repositioning, crowd starting area and exit, with a plausible solution sequence. Identify any spatial/collision ambiguity.
3. Propose a deterministic, testable **one-group shortest-path** model, including cell size or navigation representation, diagonal/cardinal movement choice, passability and recalc triggers; demonstrate how decorative dots follow the group without individual AI.
4. Identify collision/occupancy issues: player tank may not block the crowd; crowd/wall interactions and exit conditions; timer start and win/loss boundary.
5. Suggest a bounded M1 scope, files/modules to add/change, objective tests (including negative paths), actual-render browser scenarios, desktop/phone evidence and one human playtest acceptance gate.
6. Flag risks and tradeoffs, particularly readability on 320–390px phones, shortest-path clarity, crowded map geometry, accessibility and no-expenditure constraints.
7. Identify any GDD ambiguities requiring a creative decision; offer practical defaults and prefer delegated implementation choices over asking routine questions.
8. Report verified repository baseline, pin/evidence links, feasibility conclusion and precise next execution authorization needed.

**Checkpoint discipline:** This is a read/assessment assignment. If writing material artifacts, safely commit and push them on a dedicated planning branch, verify remote SHA, and provide GitHub links. Do not alter gameplay code, modify existing approved art/controls, merge, deploy or incur costs. Do not claim historical tests were rerun unless actually executed.

**Stopping condition:** Return a concise Offer and proposed acceptance criteria for owner/ChatGPT review. Wait for explicit authorization before implementing Breakthrough.
