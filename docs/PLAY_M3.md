# Interception M3 — review build

Extract the ZIP and open `guardian.html`. If local-file opening is restricted, serve the extracted folder with `python3 -m http.server 8080 --bind 127.0.0.1`, then open `http://127.0.0.1:8080/guardian.html`. The bundled HTML needs no further external requests. Managed Chromium blocked direct `file://` testing; local HTTP with every later request blocked was verified.

Choose **Interception · Level 3**, then Start mission. Move with arrows/WASD and hold Space to fire. On touch, hold a direction and Fire together. Guardian faces immediately; its fixed cannon fires once per second with unlimited ammunition.

Defeat the battleship with **six hull hits before it leaves the field**. Guardian has three HP. Enemy shells deal one damage; a hit grants three seconds of protection while movement/fire remain usable. Both losing all tank HP and letting a surviving ship escape end the attempt. There is no separate countdown: the ship's actual route is the deadline, roughly26 seconds at current defaults.

Stay on the peninsula; shells cross the coast. The visible ship hull remains hittable during turns. Its batteries stay on starboard, firing into the peninsula when aligned. A brief gun-mouth glow and HUD status warn of a coming broadside. The ship holds fire through turns/alignment gaps; bullets do not home. Reposition and use your fixed facing to find firing opportunities; smoke/fire and HP labels show damage.

Pause, confirmed retry and level exit are available. Language switches live between English/繁體中文. Sound starts muted; the note icon toggles it, and ≈ toggles reduced motion. The original Guardian range, Breakthrough and Colossus remain selectable. Short landscape screens require scrolling.

This is the bounded M3 review build for creative-director Confirm & Close, not a deployment/public release. The informed two-station strategy wins in about12.7–12.9 seconds without damage; it does not require sustained dodging after initial setup. Independent first-time-player and physical-phone tests were not performed. Original reference archival is pending receipt of the promised ZIP; accepted original ship art is included unchanged. Licensing and incomplete canvas/contrast accessibility review remain disclosed in QA/provenance.

繁體中文：選擇「攔截・第三關」並開始。方向鍵或WASD移動，空白鍵開火；觸控可同時按住方向與「開火」。在戰艦離開前命中船體六次。守護者有三點生命，受傷後保護三秒，仍可移動及射擊。注意砲口與狀態列的側射預備提示，移動尋找射擊時機。船體轉彎時仍可命中；砲彈不會追蹤。可暫停、重試、離開、切換語言、靜音及減少動態效果。
