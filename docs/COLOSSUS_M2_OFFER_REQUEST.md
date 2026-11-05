# Armorheart — Colossus (Level 2) visual and feasibility Offer request

**Date:** 2026-11-03 (Asia/Taipei). **Authorized:** assessment, original visual concepts/prototype-art feasibility and bounded implementation Offer; **NOT** full Colossus gameplay implementation, merge, deployment or public release.

## Canonical accepted starting point

- Breakthrough R3 creative acceptance including both final visual corrections: `1d6abaa4f8f98bb0034641bde855ac4b16786bed`. Accepted Guardian range and R3 gameplay are to be retained unchanged.
- Review `PROJECT_STATE.md`, `docs/ARMORHEART_GDD_v1.0.md` (especially Level 2, HP, damage and animation), `docs/QA_R3_VISUAL.md`, project-pinned UGDS/AICP, and latest shared AI-native guidance without repinning.
- Owner-supplied four-panel Kong reference sheet **KONG-01 / KONG-02 / KONG-03 / KONG-04** is in the source conversation. It is **not** a verified repository attachment; request the user to attach it to the Codex session if the executing AI cannot access it. Never claim to have inspected inaccessible original bytes or use an invented file path.

## Creative directive — intended player experience

Colossus is a giant gorilla boss whose massive form reads instantly at Armorheart's normal top-down gameplay scale. The gorilla retains an expressive face, powerful shoulders, arms and weight; the tank reads as vulnerable against it. The reference sheet is inspiration, **not a mandate to duplicate photorealistic detail**.

- Prefer **KONG-01** as foundational identity: natural dark-furred giant, imposing anatomy and strong readable silhouette; modestly borrow heroic proportions or contour exaggeration from **KONG-04** if useful, **without** elaborate weapons or armor.
- KONG-02 (cyborg armor) and KONG-03 (volcanic/mutated) are *not* the preferred production identities for this stage.
- Match the accepted Guardian/transport visual system: stylized, cohesive solid shapes, restrained shading, limited textures, clear contour and intentional color separation. Avoid photographic fur, complex surface microdetail, background composites and excessive UI overlays.
- Camera/art projection should be **elevated three-quarter**, more revealing of face, chest and arms than full bird's-eye. A useful exploratory direction is roughly **55–65° downward from horizontal**, but prioritize appearance over numeric angle. Feet/knuckles, ground shadow, jump origin and landing pose must remain spatially credible on the top-down arena.
- Primary silhouette must be distinguishable at **normal desktop and phone gameplay size**, not only in an enlarged concept. Artwork must be original, transparent and editable. Do not crop/relabel the supplied reference sheet as an in-game sprite, assert production licensing or incur costs.
- Produce coherent poses/state concepts: idle/looking around, airborne jump, landing impact, hit reaction, Fatigued and Wounded. Avoid creating a large animation pipeline before proving one representative playable-scale art sample. Test consistent perspective and form across positions/frames. A frontal render alone is not proof of four-facing or jump animation readiness.

## Original approved Level 2 rules to preserve in the Offer

- Arena is square or near-square, using accepted tank/arena engine.
- Kong jumps predictably **upper-left → upper-right → lower-right → lower-left → center → repeat**; readable next landing telegraph; **2-second pause after each landing** with recovery/looking around. Jump transit timing/size is playtest-adjustable.
- Kong has **4 HP**, with appearance stages: Intact (4), Fatigued (3–2), Wounded (1), defeated (0). Player shots deal 1 damage and are consumed on first effective hit.
- Player tank **3 HP**; Kong contact causes **1 damage** and grants **3 seconds** invulnerability, with appropriate flash and retry at zero HP.
- Kong may destroy destructible walls; whether/how to use them in this level must be assessed without inventing additional boss attacks.
- Defeat Kong to win, tank destruction to fail; **no arbitrary timer**.
- Preserve EN/zh-TW UI, keyboard/touch, pause/retry, responsive layout, reduced motion, mute, accessibility and offline behavior. No enemies/other bosses/unlock system by default.

## What Codex should return, not implement yet

1. Inspect current R3 architecture and determine the smallest reusable boss-mission adapter and damage/event model. Distinguish reusable systems from missing capabilities.
2. Propose the **visual production method** at $0: original editable concept/pose sheet and transparent sprite/layer plan, at-scale examples, animation feasibility and provenance. If generating art is not available in Codex, make an honest asset handoff contract rather than producing an inferior placeholder and claiming acceptance.
3. Offer a concrete arena layout with exact meaningful jump/landing locations, telegraph/hit windows and safe tank spawn. Show how the fixed turret can actually hit Kong while respecting 1-second firing cooldown.
4. State explicitly how jump movement, pauses, landing collisions, invulnerability and stage changes work, including any ambiguous contact rules or unintended unavoidable damage. Propose conservative defaults.
5. Plan verification: rules, real-input browser paths, damage/invulnerability edge cases, representative sprite/pose fidelity, actual desktop/phone capture, all five jump stops and transitions, bilingual/a11y and offline regressions; clear human playtest/creative gates.
6. Identify technical, art-consistency and mobile-readability risks, with a bounded execution scope and explicit next authorization. No speculative full-campaign architecture.
7. Record Breakthrough R3 owner acceptance and its limitations in durable repo history if not already reflected; do not duplicate authority claims.

**Stop at an Offer.** Write concise links and evidence to a dedicated planning branch, safely push checkpoints and verify remote SHA. $0, no force push, merge, deployment, publication, additional missions, generic art overhaul or unapproved gameplay extensions.
