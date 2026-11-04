# Armorheart — Interception M3 creative acceptance and Siege M4 Offer request

2026-11-04 Asia/Taipei. Owner reviewed playable Interception M3 at [108515a](https://github.com/jaychtw/armorheart/commit/108515a2f63c4818567d46de6bbcc0aa0611af07), reported **no obvious defects** and explicitly said **"We can proceed."** This constitutes bounded creative acceptance of the M3 playable stage. It is **not** permission to merge, deploy or publish, nor evidence of unperformed physical-device/user studies.

## A — M3 Confirm & Close (documentation only)

- Record the owner's creative acceptance, verified checkpoint, preserved tests/evidence, and known limitations in `PROJECT_STATE.md` and a concise decision/closure record.
- M3 known limitations remain: informed two-station win ~12.7–12.9s with little subsequent response, no independent first-time-player or physical-phone validation, incomplete contrast/canvas accessibility assessment, other-browser-engine and production licensing not verified, original owner battleship-reference *bytes* not archived. These are disclosed, not required blockers to this bounded creative acceptance.
- Preserve all previously accepted Guardian/R3/M2 behavior and M3 assets, rules, art and historical records. No new implementation changes requested; do not conflate reported test results with independent reruns.

## B — Stage 4 Siege (Fortress): bounded feasibility and creative Offer ONLY

Consult the repository's `docs/ARMORHEART_GDD_v1.0.md`, adopted UGDS/AICP pins, and most recent project state. This is the fourth and final planned mission, tentatively **Siege**. Prepare the smallest useful Offer for a playable fortress encounter; **no full M4 implementation** is currently authorized.

### Existing design to preserve

- Fortress is a **stationary** boss with **8 HP**: Intact (8–6), Broken (5–3), Half-destroyed (2–1), then defeated.
- Fortress shoots **five-projectile radial/fan volleys** on an initial **3-second** cadence. It may aim the fan at Guardian's position at launch, but projectiles **never home after launch**. If a volley becomes unfair/too busy, evaluate waiting until existing rounds leave the arena; do not quietly replace the core mechanic.
- Tank remains **3 HP**; a successful hit grants **3 seconds of immunity**. Guardian retains accepted 4-directional fixed gun, 1-second hold-fire, 1 damage per shell, unchanged recoil/hull/scale.
- **Cover matters:** destructible wall blocks are 1 HP and may be destroyed by either side's projectiles; indestructible barriers provide dependable geography and cannot be destroyed. These must be visually distinct and cannot secretly block shots or the Guardian.
- Win by reducing Fortress to zero HP; lose when Guardian reaches zero HP. No arbitrary mission timer. Preserve bilingual EN/zh-TW, accessible keyboard/touch, offline static build, $0.
- Maintain selected-stage structure and existing accepted game levels. Do not implement tank roster/unlocks/campaign systems under this isolated Offer.

### Explore and offer, not build the complete mission

1. Propose one clear **arena geometry**: Fortress footprint and attack origin, Guardian spawn, destructible/indestructible walls, firing lines, cover breaks and routes. Demonstrate that an intact map is neither a trivial stationary win nor an impossible firing puzzle, and that destruction can alter safety without creating unfair unavoidable damage.
2. Propose an **Armorheart-consistent fortress art direction**, with distinctive readable 2.5D top-down mass, weapon mouths, ground anchor, collision footprint, and all three damage-state silhouettes. Prioritize actual game-scale readability, not costly detail. Produce a bounded representative sample/scale proof only where feasible with available $0 capabilities; do not expand to a full art pipeline without execution authorization.
3. Explain the **five-shell fan** precisely (launch origin(s), angles, travel speeds, cadence/telegraph, collisions with destructible and steel walls, ordering when cover is hit and destroyed). Check tank escape/dodge lanes, immunities and if a fixed-cardinal Guardian has reasonable 8-hit windows. Provide mathematical or isolated motion proof as proportional evidence; distinguish it from actual-input game verification.
4. Assess a possible **cover attrition curve**: early barrier protection versus eventual wall demolition. Preserve meaningful shelter and decision space without requiring newly invented mechanics or stealth damage.
5. Return a concise Offer: bounded implementation architecture/reuse, art acceptance gate, focused test plan and gameplay-size screenshots, estimated major risks and *only material* creative choices to settle. Avoid repeated broad feasibility rounds and unnecessary standards churn.

### Execution boundaries

Task A is authorized **documentation-only closure** of accepted M3. Task B is authorized **planning, feasibility and bounded visual study only**. Do not implement Stage 4 gameplay, add novel weapons/HP or automatically tune core mechanics, merge to main, deploy, publish, force-push, spend money, or silently repin standards. You may choose ordinary technical methods autonomously and preserve safe GitHub checkpoints. Present an M4 Offer for owner review.

Optional ancillary cleanup: if the original battleship-reference archive becomes actually accessible, preserve exact bytes/verified hash and honest rights/provenance; do not block M4 Offer or claim source receipt without the bytes.
