# Colossus M2 review evidence

Technical delivery, pending creative-director Confirm & Close. [QA, measurements and remaining limits](../../docs/QA_M2.md) · [play guide](../../docs/PLAY_M2.md).

1. [Registered directional/pose gallery](registered-poses.png) and [ground registration inspector](ground-registration-inspector.png). Diagnostic ellipses in the inspector are not normal gameplay overlays.
2. [Live full five-stop cycle](cycle-live.webm) and [live emulated-touch victory](touch-safe-live.webm). Real-time Chromium compositor; no clock/state override. [Recorded timings](recording-check.json), [cycle trace](cycle-live-trace.json), [touch trace](touch-safe-live-trace.json). Both recordings are muted.
3. Actual game: [desktop airborne/rear view](cycle-07.png), [desktop entry](desktop-entry.png), [320px Traditional Chinese](viewport-320x740-zh-TW.png), [390px English](viewport-390x844-en.png). `cycle-00.png` through `cycle-10.png` show the full sequence and direction changes.
4. Combat: [Fatigued](touch-held-safe-hp2.png), [Wounded](touch-held-safe-hp1.png), [victory](touch-held-safe-victory.png), [first damage](keyboard-contact-loss-first-contact.png), [second damage](keyboard-contact-loss-second-contact.png), [defeat](keyboard-contact-loss-defeat.png). Safe-lane win is a disclosed balance issue, not evidence of meaningful forced evasion.

Reports: [83 M2 browser checks](browser-results.json), [124 unit rules](unit-tests.txt), [art/proxy checks](art-check.json), [16,080-state preservation](preservation.json), [timing parameter assessment](balance-parameter-check.json), [clean rebuild](rebuild-check.json), [ZIP integrity](package-check.json). [R3 checks](r3/browser-results.json), [Guardian checks](guardian/browser-results.json), [visual regressions](visual/visual-results.json) and [focused Guardian suite](guardian/r2-browser-results.json) are freshly run. Axe reports are `axe-{320,390,1440}-{en,zh-TW}.json`; zero reported violations does not resolve incomplete canvas/color-contrast review.

Keyboard and emulated-touch playthroughs are automated actual input. No independent first-time-player, physical-phone, other browser-engine or assistive-technology human test was performed. Previous R3/Guardian evidence remains under its original folders. Repeated legacy PNG galleries and raw recording JPEGs are excluded from Git; result reports are retained.
