# Armorheart — R2 Execution Authorization

I approve execution of the bounded R2 Guardian POC refinements, incorporating your recovery review and the following clarifications.

## 1. Owner acceptance and corrections

The previous Guardian POC has been reviewed by the creative director.

The following decisions are explicitly confirmed:

- **Barrel recoil:** Accepted. Freeze the existing mechanism and appearance unless a necessary integration fix requires a change.
- **Tank–wall collision:** Rejected in its current form. Must be corrected.
- **Muzzle flash:** Rejected in its current form. Must be replaced.
- **UI/page background:** Requires visual improvement through an appropriate military or battlefield theme.
- **Wall fragmentation:** Acceptable for the current POC. Optional improvement only.

These are owner review decisions, not inferred approvals from the earlier ZIP.

## 2. Authorized implementation

### P0 — Collision correction

Correct tank collisions against destructible and indestructible walls.

Acceptance criteria:

- The visible hull and tracks must stop at the walls' physical boundaries.
- The cannon barrel is excluded from the tank's collision geometry and may overlap a wall.
- Pressing a direction changes the tank's facing immediately, including when movement is blocked.
- Turning must not allow the hull or tracks to penetrate a wall.
- Movement parallel to walls, corners, and all four orientations must behave consistently.
- Existing movement speed and gameplay scale should remain unchanged unless a demonstrable technical issue requires escalation.

Use a suitable collision representation based on the actual tank artwork. Pixel-perfect collision is not required.

Include automated collision tests and actual desktop/mobile visual evidence.

### P1 — Muzzle-flash replacement

Replace the existing muzzle flash using the supplied references.

Preferred visual direction:

- Q-1C's directional jet, combined with a warmer, fuller muzzle blast.
- The narrow origin connects to the cannon muzzle.
- The flash expands forward in the firing direction.
- All four cardinal orientations must render correctly.
- Flash timing must remain consistent with recoil and projectile launch.

The supplied PNG contains an opaque checkerboard background. Do not display it directly with the checkerboard visible.

You may reconstruct an original transparent effect from the references using available $0 tools.

The required quality is suitable for **R2 prototype review**, not final production-art acceptance.

Document asset provenance and limitations.

### P1 — Themed UI/page background

Replace the plain page background with a restrained military-inspired visual treatment.

Preferred starting point: subtle steel-plate panels or industrial detailing.

A battlefield-inspired background is also acceptable if it integrates better with the existing game.

Requirements:

- Do not obscure the play area or gameplay elements.
- Preserve readability in English and Traditional Chinese.
- Maintain responsive desktop and mobile presentation.
- Avoid unnecessary decorative complexity or performance overhead.

### P2 — Wall fragmentation

The existing fragmentation is acceptable.

Improve only if a modest, low-risk enhancement can be made without delaying P0/P1 work.

Otherwise defer it explicitly.

## 3. Frozen and excluded scope

Preserve the previously verified:

- Four-directional movement and fixed turret.
- One-second held firing with unlimited ammunition.
- One-shot destructible walls.
- Independent barrel recoil.
- Keyboard and simultaneous touch controls.
- English/Traditional Chinese localization.
- Accessibility and reduced-motion support.
- Offline/static-browser operation.

Do not implement additional tanks, bosses, campaign missions, unlock systems, or unrelated gameplay features.

## 4. Engineering and preservation

Follow the adopted AICP v1.2.1 and pinned UGDS v1.0.0.

Use the recovered repository baseline and a dedicated development branch.

Before pushing, check repository state, conflicts, CI/deployment triggers, secrets and potential costs.

Commit and safely push meaningful intermediate checkpoints, then the final verified checkpoint.

Provide permanent GitHub commit links and reproducible review evidence.

Restrictions:

- $0 incremental expenditure.
- No force-push.
- No merge into `main`.
- No public deployment or publication.
- No unapproved scope expansion.

If safe pushing is blocked, preserve an independently durable backup where feasible and report the blocker.

## 5. Verification and final report

Run the existing regression suite, adding focused tests for corrected collision geometry.

Provide:

- Collision demonstrations from all four orientations, including corners and blocked turning.
- Muzzle-flash screenshots or recordings in all four directions.
- Desktop and mobile captures of the revised UI theme.
- Recoil regression evidence confirming the accepted behavior is preserved.
- Test results and accessibility findings.
- Updated QA report and project state.
- Final remote commit SHA and permanent GitHub links.
- Any remaining limitations or issues requiring creative-director review.

Stop after delivering R2 for Confirm & Close.

**This message is explicit authorization to implement and safely push the bounded R2 changes. It is not authorization to merge, release, deploy, or expand the game.**