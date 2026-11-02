# R2 implementation decisions — 2026-11-03 Asia/Taipei

Authority: [explicit owner execution authorization](R2_AUTHORIZATION.md). In this execution the owner additionally selected **adjust proving-ground wall placement for turning clearance**, preserving scale, speed and immediate facing, rather than allowing large nearest-clear-position shifts in narrow gaps.

## Geometry and layout

Rejected collider: 46x46 world-unit square. Replacement: conservative opaque hull/track envelope in source pixels x12..198, y70..185, pivot107,128, scale .5 => 93x57.5 world units, rotated cardinally. Does not include barrel. Source art and rendering scale unchanged. Movement clamps exactly to logical wall faces; wall decoration is inset 1–2 world units. Pixel-perfect collision not claimed. Small protrusions and transparent corners make this envelope conservative.

Immediate turns apply minimum legal center clearance only when the expanded orientation would overlap a wall or world edge. This is an instantaneous contact correction, not a speed increase or an animated turning arc. In the original layout, a sampled tight-gap turn required ~62 units; this was escalated before adopting that behavior. The owner's map adjustment removes those pockets. New bricks: (5,5),(5,2),(8,2),(8,5),(6,8),(9,8); steel: (2,2)..(2,7), in 64-unit grid cells. Six destructible blocks and six permanent blocks remain; initial center352,608 and156 units/s unchanged. Bricks are spaced so removal cannot create a narrow turn trap; steel forms a permanent test barrier. The six-block exercise is still not a campaign level.

The maximum one-axis footprint expansion is19 units. Dense intact-map tests and all64 brick-removal states sampled at24-unit spacing verify no relocation beyond this limit; sampling is not a proof over continuous space. No arbitrary turn teleport or map traversal is intended.

## Frozen behavior and visual choices

Accepted recoil function, timing, stroke, layer source and draw transforms preserved. New flash follows the moving muzzle, including its1-world-unit cross-axis offset, instead of the old fixed centerline; projectile origin/launch rules unchanged. Original transparent procedural Q-1C-inspired jet plus warm fuller bloom,90ms. CSS steel detailing, pale readable work surfaces, no runtime network assets. No background mockup used. Wall breakup explicitly deferred; acceptable existing effect unchanged.

## Review evidence

Owner input references:01_collision_right.png and02_collision_up.png (bug captures);03_muzzle_flash_supplied.png (opaque RGB reference, not runtime);04_muzzle_flash_variants.png (Q-1C directional inspiration);05_assistant_theme_mockup_reference_only.png (atmosphere only, not runtime).

Source checkpoint precedes final evidence/packaging. Historical POC evidence remains in evidence/; current run goes to evidence/r2/. Final visual acceptance is pending. No merge, hosting, publication, standards change, campaign, other tank or production-art approval.
