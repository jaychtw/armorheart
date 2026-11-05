# Breakthrough M1 — review evidence

[QA methods/results/limits](../../docs/QA_M1.md) · [Play instructions](../../docs/PLAY_M1.md). Current-run automated evidence; creative acceptance and independent human/physical-phone testing remain pending.

Review the full mission in order:

1. [Entry/instructions](desktop-entry.png), [left entrance open, crowd waiting](keyboard-left-lower-open.png).
2. [Complete route opens / localized evacuation cue](keyboard-left-evacuating.png), [Traditional Chinese](keyboard-left-evacuating-other-language.png).
3. [Keyboard success](keyboard-left-success.png), [simultaneous-touch right entrance](touch-right-lower-open.png), [touch evacuation](touch-right-evacuating.png), [touch success](touch-right-success.png).
4. [Timeout](desktop-timeout.png), [bundled offline route](offline-right-evacuating.png), [bundled success](offline-right-success.png).
5. [320px EN](viewport-320x740-en.png), [320px zh-TW](viewport-320x740-zh-TW.png), [390px EN](viewport-390x844-en.png), [390px zh-TW](viewport-390x844-zh-TW.png), [desktop EN](viewport-1440x900-en.png), [desktop zh-TW](viewport-1440x900-zh-TW.png). Tablet and short-landscape files also included; full-page captures are not single-screen claims.

Results: [51 named rule tests](unit-tests.txt), [65 mission browser checks](browser-results.json), [R2 27 checks](r2-regression/browser-results.json), [R2 81 focused checks](r2-regression/r2-browser-results.json), [unchanged Guardian assets/recoil/transform](r2-preservation.json), [recoil recording](r2-regression/guardian-recoil.webm), [offline range check](r2-regression/offline-preview-check.json), [independent archive rebuild](rebuild-check.json), [ZIP integrity](package-check.json).

Six `axe-{320,390,1440}-{en,zh-TW}.json` reports record zero violations and incomplete contrast review. Do not interpret them as full conformance. Playthroughs use actual keyboard/CDP touch controls on the running map, with Playwright time control and read-only snapshots; they are not human player tests. Simulated visibility events are labeled in the JSON.
