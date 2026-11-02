# Play Armorheart — Breakthrough M1

Extract the ZIP and open `Breakthrough-M1/guardian.html` in a modern browser. The accepted Guardian range remains the default exercise. Choose **Breakthrough · Level 1** / **突破 · 第一關**, read the instructions, then start the mission. Everything is embedded; no runtime packages, accounts or external requests.

Arrow keys / WASD move; hold Space to fire. On a phone, hold a direction and Fire together. Open either lower brick gate, enter the turning chamber and reposition toward the upper brick gate. Steel cannot be destroyed. The twelve dots are one non-blocking crowd: they wait until a complete route to the northern exit exists, then evacuate automatically. The entire group must reach the exit before90 seconds; the alternate lower gate is optional. Opening more walls is not the victory condition.

Pause, language switching, mute and reduced motion are available. Retry resets this mission, keeping settings. Level exit asks for confirmation during play and returns to the exercise chooser. No enemies, damage, campaign progression or later missions.

If local HTML is blocked, serve the extracted directory:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Use `py` instead of `python3` on Windows if needed; open the locally served `guardian.html`. Direct `file://` opening is not verified in the managed browser. The self-contained build is verified over local HTTP with all additional requests blocked.

For source development run the same server command from the repository root and use its index page. Run `npm test` for range/M1 rules. See `docs/QA_M1.md` for actual evidence, commands and limitations. This is a prototype for creative-director review. Independent first-time-player/physical-phone tests and production-art licensing are not implied by automated results.
