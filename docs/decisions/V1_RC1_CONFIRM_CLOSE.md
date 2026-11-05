# Armorheart v1.0 RC1 — owner creative acceptance / Confirm & Close

**Date:** 2026-11-05 (Asia/Taipei).

**Owner decision:** "I didn't find any issues in the play test. Approve of this RC." The owner explicitly accepts the integrated `v1.0 RC1` as the finished creative baseline, including all four previously accepted missions, four cosmetic tank designs, first-distinct-victory unlock progression, saved progress, bilingual selection/results and campaign commendation.

## Accepted candidate identity

- Verified delivered branch: `dev/v1-finalization` at [`42e98a6233faf4e126d54e05dac5806c44469489`](https://github.com/jaychtw/armorheart/commit/42e98a6233faf4e126d54e05dac5806c44469489)
- Runtime/preview source: `f1a0f2379ccddbae4a3f97dd2901743ccdadec38`.
- Review ZIP: `artifacts/Armorheart-v1.0-RC.zip`; delivered ZIP SHA-256 `6afd0bb8771494e96d9625e23f74e76e13c486061d8ace702849c5d7ad4ec466` per the recorded package check.
- [QA](../QA_V1.md), [visual evidence](../../evidence/v1/README.md), [release proposal](../V1_RELEASE_HANDOFF.md). Final runs *reported by Codex*, not independently re-executed in this closure: 183 rule tests + 1,285 browser assertions passed; 17 reconstructed outputs matched byte-for-byte.
- All four stages and the composed-game UX are creatively accepted. Prior stage baselines and intentionally accepted balance/visual limitations stay frozen. No new gameplay scope or follow-up polish is required for this creative acceptance.

## Remaining explicitly disclosed qualifications

No physical-phone, independent first-time-player, Safari/Firefox/other-browser-engine or human assistive-technology tests were performed. Canvas nonvisual accessibility/full contrast review remains incomplete; landscape may scroll; browser-local progression does not synchronize across devices. Direct file opening remains unverified. Existing R3 tank/truck overlap, M2 safe-lane, M3 fast informed win and M4 HP-trade win remain accepted limitations.

Shipping asset legal/provenance review remains incomplete, including unresolved production distribution rights and unavailable original M3 owner-reference bytes. These do **not** retract creative acceptance, but should be resolved or consciously assessed before public release; do not declare assets licensed merely because original art was generated.

## Boundary and next safe action

**Creative Confirm & Close is complete.** The owner approved RC1 **but did not expressly authorize** merge to `main`, GitHub Pages setup/deployment, release tagging, public release, or changes to the Possibility portal. No such mutation is authorized by this closure alone.

For a later, distinct release authorization, use [`docs/V1_RELEASE_HANDOFF.md`](../V1_RELEASE_HANDOFF.md), verify the current repo policies and source SHA, and revalidate any merge-generated candidate. Prepare staged/manual-only GitHub Pages publication of the single self-contained `index.html`; do not publish source/reference folders accidentally. The separate [Possibility handoff](../POSSIBILITY_HANDOFF.md) follows confirmed live publication with its own authorization.

Preserve a verified rollback identity; no force-push, paid services, hidden release setup or standard pin changes. `main` and public site remain unchanged by this record. Any future improvements should be new, explicitly scoped work, not an implicit condition on this accepted v1.0.
