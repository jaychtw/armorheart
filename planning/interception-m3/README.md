# Interception M3 — isolated Offer studies

2026-11-04 Asia/Taipei. **Planning only; no Stage3 runtime implementation.** [Owner handoff](../../docs/INTERCEPTION_M3_HANDOFF.md). Accepted M2 presentation correction is preserved separately at [94493a6](https://github.com/jaychtw/armorheart/commit/94493a6380f5fd34a6f56e059728c7b6ec69e21e).

[Exact proposal](map.json) · [map diagram](map.svg) / [PNG](evidence/map.png) · [interactive route/scale proof](proof.html) · [real-time motion](evidence/route-live.webm) · [desktop north broadside](evidence/route-1440-north-broadside.png) · [320px left turn](evidence/route-320-left-turn-45.png) · [390px right turn](evidence/route-390-right-turn-45.png).

The original editable [technical ship proxy](ship-scale-proxy.svg) tests footprint, fixed starboard mounts and rotation, using the actual accepted Guardian layers/scale for comparison. It is **not reference-matched production artwork or an approved ship identity**. The owner reference was not present in the repo/session; one attachment request was made. No claim of inspecting it, no original reference pixels used, no new paid tool/service. Final art must be compared with that reference before bulk damage-state production. Technical fixes are autonomous; a material identity mismatch needs a focused counteroffer.

The peninsula rectangle is connected to the southern edge, with open sea west/north/east. Clockwise travel leaves land on starboard on all three legs; reversing traversal makes the same fixed batteries face outward. The route consists of two north-corner radius144 circular fillets, tangent to the straight legs, at constant72 units/s. Heading stays continuous from−90° through0° to90°. Curvature/angular speed begins/ends at joins; no instantaneous heading pivot or hidden teleport. No camera/world change, fog trick or independently aiming turret.

Selected fire policy: tick every3s from3s, skip turns and any tick where one of three forward bore rays misses land. No deferred burst. Slots3/12/18/21 fire;6/9/15/24 hold. Actual intervals therefore include9s/6s gaps. Cardinal parallel shells are88 units apart, speed180, radius4; guns keep their starboard orientation while holding. Proposed0.6s local turret charge/status precedes an eligible launch; no homing. Six-shell maximum overlap is possible for the final two volleys. The diagonal curved-fire candidate was assessed and rejected as unnecessary complexity: [candidate evidence](evidence/curved-fire-candidate.json), not implemented.

Reproduce mathematical studies:

```sh
node planning/interception-m3/verify-geometry.mjs
node planning/interception-m3/assess.mjs
node planning/interception-m3/volley-escape.mjs
```

Serve the repo locally on127.0.0.1:8080, open `/planning/interception-m3/proof.html`. Play/slider inspect only route geometry; no tank input, HP combat or mission loop exists here. `python3 planning/interception-m3/capture.py` renders21 desktop/phone frames and records the full live native-RAF route with Chromium/Playwright/ffmpeg. [Render report](evidence/render-check.json), [motion trace](evidence/motion-trace.json). The recording demonstrates route continuity/rotation and clipping, not actual gameplay or production-art acceptance. Repeated raw JPEG frames are excluded from Git.

[Geometry](evidence/geometry-check.json):7,570 samples at 0.25-unit spacing route samples, exact hull-edge/land checks, conservative continuous-clearance lower bound67.47 world units; C1 position/heading continuity; all64 legal-center extreme corner/facing cases give maximum19-unit Guardian turn correction. Turn-safe center core[271.5,496.5]×[287.5,720.5] needs zero correction for any facing. Natural ship hull clipping at the north viewport reaches about2.72 world units in this proxy; initial stern/exit also clip naturally. Final artwork must be rechecked, not certified by a proxy.

[Combat assessment](evidence/combat-assessment.json): math model uses the accepted tank movement/hull functions,480/s point player shells,1s cadence and68-unit muzzle sweep; hull target is the technical polygon, not actual future art. Enemy shells are conservatively tested against swept tank AABB envelopes expanded4 units, not exact rounded-corner circle collision. Rotating target intersection is an endpoint-local approximation, convergence checked at120/240/480Hz. Player hits are clipped to the visible768-square field. This is a bounded feasibility model, not a production engine or browser playthrough.

The two-station witness: drive left0.675s; face left/hold Fire until1.9s (two hits); drive right until2.575s; face up/hold Fire. Six hits win about12.72s with3 tank HP. This proves modeled solvability, not fun or novice ease. Spawn-up held Fire lands only4/6 and loses to exit.1,568 reachable single-station camps (49 positions ×4 facings ×8 initial shot delays) found no victory, maximum5 hits; this is not exhaustive proof camping is impossible. Slower40/56 speeds permit stationary spawn victories, so72 is proposed. The informed two-station witness still requires little ongoing response after the initial reposition; no mandatory sustained dodging is claimed.

[Volley escape study](evidence/volley-escape.json):848 sampled start/volley scenarios, including legal shoreline corner states.394 stationary starts are threatened;10 need a move-stop-face response rather than one constant direction. All have at least one assessed zero-hit response beginning0.6s before launch. This is not a universal no-unavoidable-hit proof: late reactions, every continuous position, overlapping volleys and real mobile response are unverified. The0.6s warning is a proposal, not implemented feedback.

Model preservation and final actual-input keyboard/touch wins, losses/retries, damage stages, offshore player shots, shoreline turning, paused clocks, exit timing, both languages/accessibility/offline and existing-mission regressions remain **implementation acceptance work**, not passed M3 tests. No independent first-time-player/physical-phone/other-browser M3 test exists. No runtime imports from this study, no deployment/merge/publication, no cost or standards repin.
