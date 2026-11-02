# Guardian POC — technical evidence and visual review

2026-11-01, Asia/Taipei. **Bounded commitment delivered for Confirm & Close; creative-director acceptance pending.** This report applies to the Guardian POC, not the complete GDD/campaign or a release. Source and final evidence are committed together on `poc/guardian-feasibility`; see Git history for exact artifact identifiers.

## What was built

A locally bundled Canvas 2D proving ground with one reconstructed Guardian, immediate four-direction facing, cardinal movement, a fixed turret, unlimited 1-second repeat fire, independent barrel recoil, muzzle flash, synthesized optional audio, impact particles, six one-shot brick walls and six permanent steel barriers. Clear/replay, pause, restart confirmation, EN/zh-TW switching, keyboard and simultaneous touch controls, mute and reduced-motion settings are included. No tank damage, crowd, campaign, bosses, unlocks or additional tanks were added. Those GDD systems are outside the owner's narrower bounded authorization.

Native Canvas was selected from the assessed alternatives for this scene: no runtime libraries or install/build prerequisites, about 219 KB for the self-contained preview, a separate deterministic rules module, and static hosting compatibility without activating hosting. This POC does not establish a full-campaign engine decision.

## Editable construction and provenance

`assets/guardian/guardian-source.svg` is the editable mixed raster/vector source. It embeds the unchanged owner-supplied 256px Guardian master and contains named `hull` and `barrel` groups. The fixed layer masks the original barrel region; a small vector surface repair fills the area revealed during retraction. The barrel layer clips the original barrel pixels. `tools/export_guardian.py` reproducibly exports `hull.svg` and `barrel.svg` without raster editing libraries, external assets or generated replacement art.

The hull anchor is `(107,128)` in master pixels, muzzle `(243,126)`, and gun axis is parallel to positive X. Both layers rotate together through four cardinal angles; turret rotation/aiming is never independent. The only recoil transform is translation of the barrel along its local axis. See `anchors.json` and the renderer. This is reconstructed editable source, **not** recovered original layers or a fully redrawn vector asset.

Nominal recoil: 12 master pixels over 45ms, then eased recovery ending at 240ms. At gameplay scale this is 6 world units, about 5 CSS pixels on the 640px desktop arena and 2.2–2.7 CSS pixels on the tested portrait phones. Reduced motion uses 4 master pixels, omits shake (none is implemented), and reduces impact particles. Muzzle flash lasts 90ms and firing is capped at 1Hz. The stationary turret still has its mantlet; the sliding barrel retracts into it.

The captured actual-render trace contains 150 samples, with measured maximum barrel translation 11.39 master pixels and an identical hull position/facing throughout. The review video contains 174 captured compositor frames. These observations demonstrate independent movement; they do not establish aesthetic acceptance. The small repair is serviceable at play scale but not production-quality source painting. Baked light/shadow rotates with the tank, fine raster edges remain, and scale-dependent aliasing is still visible. See the enlarged in-app inspection, exploded view, cardinal sheets and recording for review.

The supplied README identifies the original as an AI-generated concept-sheet cutout. No model/provider generation record or explicit production license was supplied. Owner authorization covers this prototype and corrected development-branch preservation, not blanket production redistribution. No stock, paid art tool, font download, generated replacement artwork or outside audio was used. Sounds are synthesized locally with Web Audio and start muted. Provenance/legal naming review remains open; no repository-wide license was invented.

## Executed verification

| Verification | Result and limits |
|---|---|
| `npm test` | **11 passed, 0 failed, 0 skipped**; direct Node test runner output in `evidence/unit-tests.txt` |
| JS syntax checks | `node --check` on engine, application and localization passed |
| Python helpers | `python3 -m py_compile tools/*.py` passed |
| Asset export | Rebuilt both SVGs from editable source; runtime loads them successfully |
| Actual browser suite | **27 checks passed, 0 failed**; `tools/browser_evidence.py`, `evidence/browser-results.json` |
| Accessibility | axe-core 4.10.3, WCAG 2 A/AA + 2.1 AA tags, desktop and mobile zh-TW: **0 violations**, 24 passed audit rules each. Contrast items also remain in axe's **incomplete/manual review** list; zero violations is not complete accessibility conformance |
| Recoil capture | `tools/capture_recoil.py`: actual compositor video, 150-sample transform/state trace, fixed hull and independent barrel displacement |
| Self-contained preview | Local HTTP document loads and removes a wall using real keyboard firing with **every additional request blocked**; no JS errors. Managed Chromium rejects `file://` navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`, so direct double-click opening is **not verified** |

The 11 rules tests cover turning while blocked, cardinal movement/bounds, immediate/held fire timing, tapping without cooldown bypass, nearest-wall one-shell consumption/no piercing, wall adjacency/muzzle overlap, permanent barrier consumption, swept collision, six-block completion/replay, recoil envelope, safe settings parsing and locale key coverage. Unlimited ammunition means no ammunition inventory or cap; this is not an infinite-duration soak test.

The 27 browser checks exercise real keyboard inputs through the full six-block route, clear/replay, pause, live language/state preservation, preference reload, editable-layer inspection, all four size choices, native keyboard control activation, actual two-pointer touch move+fire, pointer release, both-language mobile UI, responsive layouts, storage-blocked/corrupt fallback and absence of JS errors/external runtime requests. The suite reads a read-only diagnostic snapshot to assert state, never mutates simulation state. No expected failures or skips were used. A preliminary audit caught contrast defects; those were corrected before the final passing run.

No CI run was introduced or claimed. No application was merged, deployed, published or verified at a public URL.

## Actual rendered sizes and devices

Chromium 154.0.8037.57, headless on the managed Linux cloud host; Node 24.19.0, npm 11.9.0, Python Playwright 1.62.0. Tests and screenshots include:

| Viewport / DPR | Arena width in CSS px | Nominal 128-world-unit sprite canvas | Visible hull thickness, approximate |
|---|---:|---:|---:|
| 320×740 / 1 | 278.4 | 46.4px | 21px |
| 390×844 / 2 | 342.8 | 57.1px | 26px |
| 768×1024 / 1 | 388.6 | 64.8px | 29px |
| 844×390 / 1 | 458.5 | 76.4px | 34px |
| 1440×900 / 2 | 640 | 106.7px | 48px |

Desktop playthrough/evidence also used 1440×1100 / DPR1. Browser comparison sheets show the assembled Guardian on **48, 64, 96 and 128 CSS-pixel canvases** using all four facings. These include source padding; actual visible vehicle size is smaller. Gameplay uses the common hull pivot; comparison thumbnails compensate for canvas centering to avoid clipping the barrel. Canvas backing resolution follows actual CSS size up to DPR2, without changing world geometry.

No horizontal overflow was found at the measured viewports; D-pad targets are 44×44 CSS px and Fire is 88–94px. The primary touch trial used Chromium's actual two-touch input dispatch at 390×844 / DPR2: tank moved from x352 to x544.4 while firing two shells, then stopped firing after release. Touch sliding, physical finger ergonomics and all pointer interruption combinations are not comprehensively verified. Portrait is the useful touch-review layout. Short landscape requires vertical scrolling; simultaneous full-field visibility and controls in short landscape is **not established**. Do not treat its no-overflow screenshot as a completed usability acceptance test.

Visual assessment: the Guardian remains recognizable in all four directions, with no independent turret drift or obvious frame discontinuity. At narrow-phone play size, tracks/hull and barrel are readable but fine fittings merge into texture; the 96/128px inspection view is substantially clearer. The fixed-axis recoil is genuine layer movement, but its ~2px phone displacement is subtle. This supports further visual review, not an assertion that the production art target is achieved.

## Evidence index

- `desktop-entry.png`, `desktop-first-impact.png`, `desktop-recoil.png`, `desktop-range-cleared.png`: entry, shooting, collision and complete/replay state.
- `desktop-layer-inspection.png`, `layered-guardian-closeup.png`: same runtime assets, including separated layer inspection.
- `guardian-recoil.webm`, `recoil-render-trace.json`: real-time recoil/flash/impact recording and measured independent motion.
- `cardinal-48px.png`, `cardinal-64px.png`, `cardinal-96px.png`, `cardinal-128px.png`: actual browser-rendered size/facing comparisons.
- `mobile-390-touch.png`, `mobile-390-zh-TW.png`, `desktop-zh-TW.png`: touch/bilingual states.
- `viewport-*.png`: responsive screenshots with dimensions/DPR in filenames. Full-page captures are taller than viewports; they are not claims that all content fits on one screen.
- JSON/text reports: browser checks, axe results, frame sample, offline preview and unit tests.

The 90-frame desktop **idle** render sample had median 16.7ms and maximum 16.8ms on this host. This is a limited local observation, not ordinary-phone performance proof, sustained combat profiling or a 60fps guarantee. No external runtime request was observed. No heap/GPU memory claim is made.

## Production recommendation and remaining gates

Functional feasibility for this bounded Guardian scene is supported by the executed evidence. **Visual acceptance remains pending with the creative director.** Physical devices, Safari/WebKit, Firefox, independent first-time-player testing, screen-reader gameplay, comprehensive canvas contrast review, touch ergonomics and sustained mobile performance remain unverified. The canvas has labels, keyboard controls and DOM status/controls, but does not offer a complete nonvisual spatial representation.

For production, retain an editable layered master with painted underlying surfaces, consistent hull/muzzle anchors, edge padding, separate lighting/shadows, and controlled downsampling. Review on actual phone screens before scaling art. If the phone silhouette/recoil is insufficient, return with a scoped art/layout counteroffer; do not silently enlarge hitboxes, crop the arena or substitute lower-quality artwork. Do not reconstruct other tanks or author bosses without new authorization.

Project-specific lesson: independent layer motion is inexpensive; correct underlying surfaces, pivot placement and rendered CSS scale are the art-production risks. Record that in this project; no standards change is proposed. This closes engineering delivery of this bounded POC and returns the evidence for owner acceptance, conditional acceptance or redirection. No further implementation is authorized by a passing test or checkpoint push.
