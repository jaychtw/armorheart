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

Once Task A is safely preserved, inspect the current repo/GDD/art pipeline and propose the smallest practical implementation of the approved Stage 3 battleship mission. **The owner's peninsula narrative and continuous turns below supersede earlier canal/sharp-corner interpretations of the GDD.** Existing mechanical GDD baseline:

- Battleship HP **6**, visual stages Intact (6–5), Smoking (4–3), On fire (2–1).
- Moves along an **inverted-U path at sea around a peninsula**: one side of the landmass → curved upper corner → northern coast → curved upper corner → opposite side → exit. Guardian defends from the peninsula; the battleship is not sailing in an upside-down canal. The ship fires **three-projectile volleys every 3 seconds**, using the baseline inward directions on the legs/top when broadside alignment makes them physically coherent. No homing.
- Tank remains **3 HP** with 3-second post-hit immunity. Lose if ship exits alive or tank reaches 0 HP; win if ship reaches 0 HP before exit. Maintain one-hit projectiles, fixed turret, cardinal controls, EN/zh-TW, touch, offline, accessibility and $0.

### Accepted narrative geography and corner treatment — binding creative directive

- The arena represents a **peninsula surrounded by sea on three sides**. Guardian occupies the land, and the hostile ship cruises around it to bombard the defender. The narrative matters: do not describe this as a canal or land-enclosed U-shaped waterway.
- At the two upper corners the battleship executes **continuous curved turns**, preserving momentum and heading continuity. No instantaneous 90-degree pivot, teleport, disappearing into clouds/fog, or cloud-concealed transition.
- The bow/stern or other parts of the vessel **may extend beyond the visible game area during cornering**, with natural viewport clipping; this is an accepted artistic result, not a collision defect. Choose a smooth path/turn radius consistent with the ship's visible scale. Do not change gameplay field/world dimensions without a compelling assessed reason.
- Preserve **main turret/bore orientation toward starboard**, approximately perpendicular to the hull. When the ship's heading rotates around a corner, the turrets rotate *with the ship* unless a distinct independently rotating turret model is explicitly proposed and accepted. Align actual three-shell volleys with the visible gun direction: if the fixed starboard broadside cannot reasonably hit the peninsula during part of a curved turn, use an intelligible firing window/hold rather than shells emitted in a contradictory direction. Examine orientation on each leg: a fixed starboard broadside can point away from land on one leg of a U-shaped route; identify this explicitly, and offer a physically and narratively coherent solution rather than silently violating either the owner's starboard aesthetic or attack-direction premise.
- The corner-turn presentation and starboard-fire coherence are **acceptance-critical**. Return at-scale route/ship rotation frames or an inexpensive motion proof before committing to bulk asset/logic production. Do not use a cinematic fog trick instead of geometric continuity.

### Owner's battleship art direction

Owner supplied a reference photograph/concept of a classic battleship with visible deck, superstructure and multiple large turrets, and explicitly requested that **turrets and barrels be turned to starboard**, perpendicular to the hull. Interpret the reference as **visual inspiration**, not necessarily production-ready art. Match Armorheart's stylized top-down/2.5D visual system; avoid excessive photorealistic surface detail. Use the accepted starboard orientation and address the port/starboard exposure implications of the proposed clockwise/counterclockwise route; make firing direction visually and mechanically consistent. The source reference image was provided in the ChatGPT conversation and is **not verified in this repository**. If unavailable in Codex, request it to be attached once; do not claim to have fetched the image from a local path.

### Offer deliverables

1. A coherent ship identity and at-scale art direction, including a transparent sprite/layer plan (hull, rotating or fixed broadside turrets, muzzle/volley effects, damage states), gameplay-size sample and editable originals if affordable with existing resources. Asset gate before bulk animation.
2. A proposed exact peninsula/sea map and continuous inverted-U curve geometry, ship centerline/heading/orientation across both corners, viewport clipping, broadside firing windows/trajectory and practical screen-size/phone readability assessment. Include a simple diagram/motion proof and explicitly resolve any leg where fixed starboard guns face away from Guardian.
3. Concrete fairness analysis: 3-shot volley spread, cadence, shell speeds, ship speed, hit windows and whether a fixed-turret Guardian can defeat it before exit. Surface stationary safe-lane exploits and unavoidable hits. Do not silently add attacks/HP or change the GDD.
4. Bounded implementation scope, reusable engine components, risk-proportionate tests, actual-input browser loops, screenshots/video, regression requirements and clear acceptance conditions.
5. A compact Offer with unresolved *material* creative choices only. Avoid repeating lengthy standards or already accepted decisions. Preserve valuable planning artifacts at verified GitHub checkpoints.

**Scope boundary:** Task A is authorized to execute; Task B is **planning/Offer only**. No Stage 3 game implementation, unapproved asset production expansion, new tank systems, force-push, merge, public deployment, extra spending or standards-pin modifications. Preserve existing project-pinned UGDS/AICP, applying relevant shared AI-native guidance without silent repinning. Report Task A completion and the Interception Offer separately.
