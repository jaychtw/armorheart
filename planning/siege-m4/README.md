# Siege M4 — isolated planning study

2026-11-04 Asia/Taipei. **Proposed, not gameplay implementation or creative acceptance.** [Authoritative Offer](../../docs/offers/SIEGE_M4_OFFER.md) · [owner assignment](../../docs/SIEGE_M4_OFFER_REQUEST.md) · [M3 closure](../../docs/decisions/M3_CONFIRM_CLOSE.md).

- [Exact map/initial parameters](map.json), [coordinate diagram](evidence/map.svg).
- [Continuous clearance](evidence/clearance-certificate.json): all16 removal masks/12 facing pairs, actual accepted hulls, bound19 units. Reuses the established R3 continuous proof with variable-size rectangles; all legal partition edges and vertices are included.
- [Predetermined motion/ray study](evidence/feasibility.json):64 physical routes;32 shelter timelines over all16 masks;24 stationary-after-approach samples. Contact/opportunity timings are analytical planning evidence, **not actual keyboard/touch playtests or an implemented M4 rule controller**. The24 samples reveal14 fast damage-trade clears; the Offer explicitly asks about this material risk.
- [Static editable art/scale viewer](review.html), [original vector master](art/fortress-study.svg), [320px](evidence/study-320-en-intact.png), [390px](evidence/study-390-en-intact.png), [Broken](evidence/study-390-en-broken.png), [Half-destroyed](evidence/study-390-en-half.png), [zh-TW](evidence/study-390-zh-TW-intact.png), [render/registration check](evidence/render-check.json).
- [Preservation](evidence/preservation.json): accepted runtime/assets/previews/ZIPs/tests and existing utilities unchanged. The preceding148 rule/615 browser results are historical; no rerun is claimed for this documentation/study task.

Reproduce from repository root with Node≥20/Python3; Chromium154.0.8037.57 and Playwright1.62.0 are development-only render tools:

```sh
python3 planning/siege-m4/certify_clearance.py
node planning/siege-m4/assess.mjs
python3 planning/siege-m4/draw_map.py
python3 planning/siege-m4/art/build_study.py
python3 planning/siege-m4/render_study.py
```

The render tool starts a temporary loopback-only server on8082, measures the accepted game's canvas at each viewport, then renders the static study at that exact CSS width. No game source is edited. To inspect the viewer manually, serve the repository locally and open `/planning/siege-m4/review.html`; controls switch static art/state samples only. It has no Guardian movement, combat state or playable level. No new ZIP is needed for this Offer.

Art provenance: the original vector construction is authored in `art/build_study.py` for this assessment, with editable stage groups in `fortress-study.svg`. No external fortress image, copied game art, paid model/service, photoreal master or production license is claimed. Guardian layers are the unchanged accepted project assets, merely rendered for scale with barrel beneath hull. Existing Guardian provenance restrictions still apply. Palette and bevels propose broad warm-stone/olive mass; material finish is flatter than Guardian and is not automatically accepted production quality. All states keep a visibly solid foundation at the unchanged proposed footprint. Future integration must register the selected rotating barrel/muzzle rather than reuse this south-facing static sample for every bearing.

No physical phone, independent player, other browser engine or M4 accessibility/performance/gameplay verification was performed. Static English/zh-TW study layout/scale checks are distinct from those future gates. No merge, deployment, publication, expense or standards changes.
