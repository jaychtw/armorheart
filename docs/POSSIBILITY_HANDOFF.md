# Future Possibility Games entry — Armorheart

**Subsequent status, November5,2026:** owner accepted RC1 and separately authorized both publications; game and Possibility are now deployed and verified. [Final receipt/rollback](V1_PUBLICATION_RECEIPT.md). The following remains the historical planning/RC verification record.

**Prepared only; not published and no cross-repository write.** Independent Armorheart deployment is also not started/not authorized. Final candidate acceptance alone is not release authority.

## Current conventions inspected read-only

Portal repository: `jaychtw/jaychtw.github.io`, main `20608379166853fe3704f1bbff858e1488d7f7e2` at inspection. No existing `armorheart.json` entry. Recheck current source before any later write:

- [Catalog contract](https://github.com/jaychtw/jaychtw.github.io/blob/20608379166853fe3704f1bbff858e1488d7f7e2/docs/CATALOG.md)
- [Maintenance](https://github.com/jaychtw/jaychtw.github.io/blob/20608379166853fe3704f1bbff858e1488d7f7e2/docs/MAINTENANCE.md)
- [Deployment gate](https://github.com/jaychtw/jaychtw.github.io/blob/20608379166853fe3704f1bbff858e1488d7f7e2/docs/DEPLOYMENT.md)

One curated JSON at `content/projects/games/armorheart.json`; stable ID, no duplicate. `title`/`summary` are English on cards. Optional `summaryZhTW` is fact-sheet text with language markup; do not invent a portal-wide language switch. Games sort newest-first by actual `publishedAt`, not commit date. Do not add an editorial pin. `status` must reflect review/publication, and `maturity` must honestly reflect the independently released project.

## Proposed content, to finalize only after game publication

- Title: **Armorheart**. English summary: “Four tank missions: open an evacuation route, confront a giant gorilla, intercept a battleship and defeat a fortress. Earn a collection of four cosmetic tanks.”
- Optional Traditional Chinese summary:「四個戰車任務：打通撤離路線、迎戰巨獸、攔截戰艦、攻克砲壘。首次完成不同任務可逐步收藏四款戰車外觀。」
- `id: armorheart`, `category: games`, `repositoryUrl: https://github.com/jaychtw/armorheart`, `languages: [en, zh-TW]`. Suggested existing-compatible tags: Action; check current tag conventions before adding any.
- Controls: Arrows/WASD move, hold Space to fire; simultaneous direction/Fire touch controls; pause, retry, language, mute and reduced motion.
- `destination.action: play`; use the **actually verified HTTPS game URL**, not an unobserved proposal. `publishedAt: null` until known. Release version/full source SHA must identify the actual public release, not this handoff or an unrelated documentation commit. Do not set `status: published` prematurely.
- Approval URL/note: eventual final integrated acceptance **and separate release authorization**, accurately distinguished from four accepted stages. Current finalization authority permits neither publication.
- Limitations: device/browser-local progress, short-landscape scrolling, unperformed physical-phone/other-engine/independent-player/assistive-technology tests and accepted informed fast strategies. Do not advertise unique tank abilities; all four cosmetics share the same mechanics.
- Thumbnail: an authentic runtime screenshot from the released artifact, or `null`/neutral fallback under current portal rules. Current [v1 evidence](../evidence/v1/README.md) is candidate evidence, not an independently published build. No custom portal cover has been approved; do not invent one.

After authorized game publication, record dated successful normal-TLS destination observations in `content/link-verification.json` using the portal's current schema/tool. Register any screenshot source/rights in `content/asset-provenance.json`; run catalog, image, rendering, accessibility, public-link and release checks. Never fabricate link evidence or infer dates from repository history. Reuse the stable entry for updates.

Current portal publication is the manual **Publish approved Possibility release** workflow, full `release_commit` SHA and guard `PUBLISH POSSIBILITY`; the guard does not confer authority. Main pushes validate only; automatic publication is disabled. Obtain separate explicit approval, merge/validate the exact reviewed portal SHA under current policy, dispatch only when authorized, then independently verify public build identity, Games card, fact sheet, screenshot and game destination. A successful portal commit/check does not prove publication. Record game deployment and portal entry publication as separate outcomes and preserve their independent rollback references. No site-wide redesign/localization/governance change belongs in this entry task.
