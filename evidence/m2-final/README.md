# M2 accepted presentation correction

2026-11-04 Asia/Taipei. [Owner decision and scope](../../docs/decisions/M2_FINAL_PRESENTATION.md). Accepted M2 build4cef3e5 is the baseline; the safe-lane limitation is accepted. No gameplay/art/physics changes.

[Desktop before](before-1440-airborne.png) / [after](after-1440-airborne.png); [390px before](before-390-airborne.png) / [after](after-390-airborne.png); [320px zh-TW before](before-320-ground.png) / [after](after-320-ground.png). Each viewport has ground, airborne and landing pairs. Natural shadow remains identical; battlefield Next text/separate landing ellipse are gone, with no substitute. Redundant Next HUD field removed; grounded/airborne, health, protection and landing announcements retained.

[Visual proof](visual-check.json):9 actual before/after pairs, identical simulation states and exact shadow expression; every boss frame/model/engine/previous M2 ZIP unchanged. [124 rules](unit-tests.txt), [83 M2 browser checks](regression/browser-results.json), [R3 regression](r3/browser-results.json), [16,080 accepted-engine comparisons](preservation.json). Browser checks use real keyboard/CDP touch, wins/losses/retry, bilingual layouts, accessibility audits and network-blocked offline play. Before rendering serves the accepted app/strings through a read-only browser route; no gameplay-state injection.

Run `python3 tools/m2_final_visual.py`; run `EVIDENCE_DIR=evidence/m2-final/regression EVIDENCE_DATE='2026-11-04 Asia/Taipei' python3 tools/m2_browser.py`, and `EVIDENCE_DIR=evidence/m2-final/r3 python3 tools/r3_browser.py` with source served locally on8080 and existing local axe/Chromium setup. Repeated regression screenshot galleries/raw frames are omitted from Git. [Corrected play guide](../../docs/PLAY_M2_FINAL.md).

No independent first-time-player, physical-phone or other-engine test performed. Axe reports0 violations but canvas/contrast review remains incomplete; production licensing unresolved. No deployment, publication, merge or new expense. Earlier M2 evidence remains historical and unchanged.
