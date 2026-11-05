# Armorheart v1.0 RC1 — visual and verification evidence

**Subsequent status, November5,2026:** owner accepted RC1 and separately authorized both publications; game and Possibility are now deployed and verified. [Final receipt/rollback](../../docs/V1_PUBLICATION_RECEIPT.md). The following remains the historical planning/RC verification record.

2026-11-04. Actual integrated build frames and reproducible reports for **final Confirm & Close**. Four individual missions accepted; integrated game/new collection awaiting creative review. [Play](../../docs/PLAY_V1.md) · [QA/methods/limitations](../../docs/QA_V1.md) · [state](../../PROJECT_STATE.md).

## Review first

- **[Normal-speed complete touch campaign](campaign-native.webm)**:69.18seconds, 1,957 compositor frames; Siege/Guardian → Interception/Bulwark → Colossus/Vanguard → Breakthrough/Sentinel, then campaign commendation. Genuine earned progress, no virtual clock/save/gameplay fixtures. [Measurements](native-recording.json), [read-only trace](native-trace.json), [final collection](native-collection-complete.png). Phone emulation, not physical hardware or independent human play.
- **Collection:** [fresh320px English](menu-320-en-count0.png), [complete390px English](touch-collection-complete.png), [complete320px Traditional Chinese](menu-320-zh-TW-count4.png), [desktop](menu-1440-en-count4.png). Distinct original designs; no abilities/stats differ.
- **Results:** [first unlock320px English](result-320-en.png), [first unlock320px Chinese](result-320-zh-TW.png), [fourth-clear commendation](keyboard-commendation.png), [selected-tank defeat/no reward](campaign-defeat-no-reward.png). Next opens the next numbered mission; Siege has no Next even if first cleared.
- **Actual art at gameplay scale:** [Bulwark facing up](bulwark-ArrowUp-rest.png), [Vanguard firing at320px](game-320-vanguard.png), [Sentinel left recoil](sentinel-ArrowLeft-recoil.png), [Sentinel simultaneous touch](sentinel-touch-simultaneous.png). All four skins have committed `*-Arrow{Up,Right,Down,Left}-{rest,recoil}.png` pairs. [Physical input trace](cosmetic-traces.json), [all-skin checks](cosmetics-browser.json). [Enlarged chart](assets/enlarged-collection.png) is separately labeled inspection scale.
- **Real native mission results:** [M4](native-siege-victory.png), [M3](native-interception-victory.png), [M2](native-colossus-victory.png), [R3/commendation](native-breakthrough-victory.png). Additional controlled-clock keyboard/touch/offline win frames remain in this folder.
- **Storage/responsive:** [denied storage session](denied-save-state.png), [unknown future version](future-save-state.png), [short landscape](menu-844-en-count4.png), [static prefix/Chinese reload](static-prefix-zh-TW.png). Deliberate saved-state fixtures are labeled in reports; they are not passed off as naturally earned campaigns.

## Reports

[183 rule tests](unit-tests.txt). [470 integrated checks](browser-results.json): [campaign172](campaign-browser.json), [cosmetics141](cosmetics-browser.json), [storage62](storage-browser.json), [layout60](layout-browser.json), [keyboard/contrast/access35](access-browser.json). Runtime hash must match across phases. Three main real-input campaigns contain13 wins including one repeat, plus additional labeled cases and a separate four-win native recording. No human-player count is inferred.

**815 freshly rerun legacy checks:** [M4/200](legacy/m4/browser-results.json), [M3/104](legacy/m3/browser-results.json), [M2/83](legacy/m2/browser-results.json), [R3/122](legacy/r3/browser-results.json), [Guardian R2/81](legacy/r2/r2-browser-results.json), [original range/27](legacy/range/browser-results.json), [visual completion/198](legacy/visual/visual-results.json). Combined final browser total **1,285**. Legacy recoil/visual fixtures and positive controls retain their explicit labels. Repeated legacy PNGs/raw recording JPEGs are excluded; prior historical galleries are untouched.

[Initial M4 timing discrepancy](legacy/m4/initial-attempt.txt):29.815s tactical touch exceeded the old20–27s check; unchanged rerun23.815s passed. Cause is not established, no game change or bound weakening. [Initial range harness issue](legacy/range/initial-attempt.txt):query prefix misclassified same-origin resources; corrected to parsed-origin comparison. These attempts are not counted as passed.

[34,080 matching baseline states / byte preservation](preservation.json), [art alpha/silhouette/registration](assets/asset-check.json), [six numeric contrast pairs](contrast-check.json), [17-output clean reconstruction](rebuild-check.json), [ZIP integrity/hash](package-check.json), [local static prefix/actual win](static-check.json), [read-only release/portal audit](release-audit.json). All 34 axe reports in this folder/tree show zero violations but retain incomplete contrast/canvas items.

## Interpretation and remaining limits

Controlled-clock checks use actual keyboard/CDP touch and production rendering with read-only snapshots/forwarding Canvas measurements. Storage fixtures isolate validation/equivalence; native campaign recording has none. The assistant inspected actual desktop/phone collection, small bilingual result, representative all-skin poses and a native video frame. That is technical/assistant visual review, **not owner creative acceptance or independent first-time-player testing**.

No physical-phone, other-engine, human assistive-technology or direct-file verification. Numeric palette checks/axe do not certify full changing-canvas contrast or nonvisual gameplay. Native timing is managed-host data, not a device performance promise. Accepted mission balance/pass-through limits, local-save constraints, licensing and unavailable original M3-reference archival remain disclosed. No merge, deployment, publication or paid resources; see [proposed release handoff](../../docs/V1_RELEASE_HANDOFF.md).
