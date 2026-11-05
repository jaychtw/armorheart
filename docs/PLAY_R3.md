# Play Armorheart — Breakthrough R3

Extract `Armorheart-Breakthrough-R3.zip`. Open `Breakthrough-R3/guardian.html`, choose **Breakthrough · Level 1** / **突破 · 第一關**, then Start mission. The accepted Guardian range is still the default scene. The build embeds all code, artwork and styles; no account, package install or external request is needed.

Move with arrows/WASD and hold Space to fire. On touch, hold a direction and Fire together; release to stop. Each effective shot removes exactly one brick cell. Steel stays. Clear both upper brick cells to open a route into the northern refuge. Leave the lower brick column intact for the longer S-bend bypass, or remove its two cells as well for the shorter truck route. Lower demolition is optional. The covered transport waits until a complete route exists, then drives and pivots automatically. Its entire body must park north-facing inside the refuge before the provisional 90-second deadline. Clearing all bricks or reaching the exit with Guardian alone does not win.

Pause freezes the clock and truck, including midway through a turn. Language, mute and reduced-motion controls remain available. Retry restores cells, vehicles and clock while preserving settings. Level exit asks for confirmation during play and returns to the Guardian range. The transport is non-blocking and immune to shots; no pushing, enemies, fuel or additional missions.

If local-file access is blocked, serve the extracted directory locally:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open the corresponding `guardian.html` URL on that machine. On Windows, `py` may replace `python3`. Direct double-click (`file://`) opening was not verified because the managed browser prohibits it. Both mission solutions were verified over local HTTP with every subsequent network request blocked.

On narrow portrait screens, arena and Fire fit together at the tested 320×740 and 390×844 sizes. Page navigation still exists; short landscape requires scrolling. Emulated touch evidence is not physical-phone testing. See [QA_R3.md](QA_R3.md) for results and pending human review. This build is for creative-director Confirm & Close; no production-art approval or release is implied.
