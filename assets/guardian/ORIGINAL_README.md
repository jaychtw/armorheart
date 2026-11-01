# Tank Prototype v0.1 — extracted visual test sprites

These are **experimental raster cutouts** from an AI-generated concept sheet, not approved production art. Foreground extraction can leave dark fringes, shadows, or incomplete antenna/barrel pixels. Review all sprites at actual gameplay scale.

Tank references: T01 Guardian (A-1), T02 Bulwark (C-1), T03 Vanguard (E-1), T04 Sentinel (S-1). These names are temporary.

Each tank has a 256x256 transparent master cutout and 4 directions in 128x128 and 64x64 transparent RGBA PNG. One original right-facing image is rotated for other directions. **No finished recoil animation is included:** implement barrel recoil as a separate transform or request properly layered sprite assets.

All stats identical, cosmetic-only (proposal, not approved). Physics/collision use consistent hull-sized hitboxes, not the outer PNG bounding box. 64x64 is an initial test target, not an approved in-game size. Verify aliasing and readability.

Do not treat background textures, overlays, labels, or shadows in the original sheet as game assets. Do not claim these sprites are final-quality or faithfully engineered tank structures. Avoid committing asset sources without inspecting license/provenance and maintaining a clean source record.

## Codex evaluation targets
1. Verify proper alpha, silhouettes, and readability at 64px in a game viewport.
2. Compare 64px vs 128px downsampling and actual pixel footprint.
3. Validate immediate cardinal facing and movement despite collision.
4. Test one-second fire cooldown with held Fire and a procedurally animated barrel recoil.
5. Measure transparent-edge artifacts and determine whether a redrawn/vector or layered asset pipeline is needed.
6. Evaluate memory, rendering performance, accessibility, and crispness on desktop/touch.

No merge, publish, or deployment authorized.
