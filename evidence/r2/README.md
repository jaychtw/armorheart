# R2 owner review evidence

Current-run evidence; historical POC evidence remains in the parent directory. See [QA report](../../docs/QA_REPORT.md) for commands, counts and limits.

Review in this order:

1. Collision contact: [desktop brick/right](collision-1440-brick-right.png), [phone steel/up](collision-390-steel-up.png), [adjacent corner](collision-corner.png). Files `collision-{1440,390}-{brick,steel}-{up,right,down,left}.png` cover both wall types and all four orientations. Fixture scene initialization only; real keyboard input, actual renderer and SVG-pixel checks.
2. Flash: [right](flash-1440-steel-right.png), [up](flash-1440-steel-up.png), [left](flash-390-steel-left.png), [down](flash-390-steel-down.png). Matching desktop/phone and brick/steel files cover all orientations. Frozen-clock real shot captures show transient effect without timing races.
3. Theme: [desktop EN](theme-1440-en.png), [desktop zh-TW](theme-1440-zh-TW.png), [320px EN](theme-320-en.png), [320px zh-TW](theme-320-zh-TW.png), [390px EN](theme-390-en.png), [390px zh-TW](theme-390-zh-TW.png). Full-page captures are not single-screen usability claims.
4. Recoil: [recording](guardian-recoil.webm), [render trace](recoil-render-trace.json), [unchanged-source comparison](recoil-baseline-comparison.json).

Results: [24 rule tests](unit-tests.txt), [27 existing browser checks](browser-results.json), [81 R2 checks](r2-browser-results.json), [all brick-removal subsets sampled](map-clearance.json), [desktop axe](axe-desktop.json), [phone axe](axe-mobile.json), [representative text contrast](contrast-review.json), [self-contained preview](offline-preview-check.json), [ZIP integrity](package-check.json).

Visual acceptance, physical phones, other browser engines and production-art rights remain open. No deployment or release is represented here. Wall-fragment improvement was deferred; accepted recoil is unchanged.
