# Armorheart — Colossus final presentation correction + Interception M3 discovery

**Owner direction:** Colossus M2 is creatively approved at `4cef3e58a7a4b244a8630e29751b71e4006a7785`, subject only to removing two redundant landing-telegraph elements. After that bounded correction, proceed to **Stage 3: Interception** discovery/Offer. Date: 2026-11-04 (Asia/Taipei).

## Task A — Complete Colossus presentation (authorized implementation)

- Remove the literal `Next` label **from the battlefield** and the separate dashed/translucent **next-landing indicator ellipse**. Do not replace either with another marker, text callout or warning ring.
- Preserve Colossus's **natural existing shadow** (do not remove or redesign it); no new shadow animation or telegraph behavior is requested. Existing phase/health UI may remain except any redundant `Next` field specifically tied to the removed indicator; keep necessary accessible announcements and understandable grounded/airborne status.
- The owner has deliberately chosen this simpler presentation despite the loss of explicit advance landing targeting. Do not add substitute telegraphs without new owner direction.
- Preserve approved 28-frame art, jump path, pauses, HP, contact/hit, Guardian controls, recoil, bilingual UI, offline builds and all existing missions. Existing safe-lane strategy is an accepted M2 balance limitation, not a mandate to retune it.
- Make the smallest viable code change (the prior renderer draws ellipse/text together in `src/app.mjs`), update tests that assert the old marker, and capture before/after desktop/phone evidence. Run focused M2 and appropriate regression tests, build an updated playable offline preview/ZIP with honest verification.
- Record owner's final M2 approval and this design correction in `PROJECT_STATE.md` and decision history, noting unperformed first-time-player/physical-phone tests and remaining legal/accessibility caveats.
- Commit/push correction on a dedicated safe development branch and report the verified remote SHA. Do not merge/deploy/publish or incur cost.

## Task B — Interception (Level 3) bounded Offer (authorized planning, NOT implementation)

Once Task A is safely preserved, inspect the current repo/GDD/art pipeline and propose the smallest practical implementation of the approved Stage 3 battleship mission. Existing GDD baseline:

- Battleship HP **6**, visual stages Intact (6–5), Smoking (4–3), On fire (2–1).
- Moves along a **perimeter upside-down U path**, one side → top → opposite side → exit. Enemy fires **three-projectile volleys every 3 seconds**, horizontally inward from vertical legs, vertically inward from top. No homing.
- Tank remains **3 HP** with 3-second post-hit immunity. Lose if ship exits alive or tank reaches 0 HP; win if ship reaches 0 HP before exit. Maintain one-hit projectiles, fixed turret, cardinal controls, EN/zh-TW, touch, offline, accessibility and $0.

### Owner's battleship art direction

Owner supplied a reference photograph/concept of a classic battleship with visible deck, superstructure and multiple large turrets, and explicitly requested that **turrets and barrels be turned to starboard**, perpendicular to the hull. Interpret the reference as **visual inspiration**, not necessarily production-ready art. Match Armorheart's stylized top-down/2.5D visual system; avoid excessive photorealistic surface detail. Decide how turret orientation behaves when the ship traverses the U so the visual gun direction and gameplay volleys remain coherent. The source reference image was provided in the ChatGPT conversation and is **not verified in this repository**. If unavailable in Codex, request it to be attached once; do not claim to have fetched the image from a local path.

### Offer deliverables

1. A coherent ship identity and at-scale art direction, including a transparent sprite/layer plan (hull, rotating or fixed broadside turrets, muzzle/volley effects, damage states), gameplay-size sample and editable originals if affordable with existing resources. Asset gate before bulk animation.
2. A proposed exact square-arena/U-path geometry, facing/orientation/broadside behavior and practical screen-size/phone readability assessment.
3. Concrete fairness analysis: 3-shot volley spread, cadence, shell speeds, ship speed, hit windows and whether a fixed-turret Guardian can defeat it before exit. Surface stationary safe-lane exploits and unavoidable hits. Do not silently add attacks/HP or change the GDD.
4. Bounded implementation scope, reusable engine components, risk-proportionate tests, actual-input browser loops, screenshots/video, regression requirements and clear acceptance conditions.
5. A compact Offer with unresolved *material* creative choices only. Avoid repeating lengthy standards or already accepted decisions. Preserve valuable planning artifacts at verified GitHub checkpoints.

**Scope boundary:** Task A is authorized to execute; Task B is **planning/Offer only**. No Stage 3 game implementation, unapproved asset production expansion, new tank systems, force-push, merge, public deployment, extra spending or standards-pin modifications. Preserve existing project-pinned UGDS/AICP, applying relevant shared AI-native guidance without silent repinning. Report Task A completion and the Interception Offer separately.
