# Siege M4 — playable review build

Extract the ZIP and open `guardian.html`. If local-file opening is restricted, serve the extracted folder with `python3 -m http.server 8080 --bind 127.0.0.1` and open `http://127.0.0.1:8080/guardian.html`. The HTML embeds all five scenes and their assets; it makes no subsequent runtime requests. Managed Chromium blocked direct `file://` testing, so that mode remains unverified; local HTTP with later requests blocked was exercised.

Choose **Siege · Level4**, then Start mission. Arrows/WASD move and immediately face Guardian; hold Space to fire once per second. Touch supports holding a direction and Fire together. The accepted fixed cannon, scale, movement and recoil are unchanged.

Hit the stationary Fortress **eight times**. Guardian has **three HP**; an effective hit grants **three seconds of protection**, with movement/fire still usable. Five enemy shells fan from the preparing roof gun every three seconds. Watch its0.6-second warning: it tracks until launch, then the rounds travel straight without homing. Damage states change the fortress artwork, not its attacks. There is no mission timer. Destroying the Fortress wins; losing all tank HP fails. Retry resets the current stage and its cover.

Brick cells shield either side once, then disappear; steel and the northern barriers remain. Each projectile is consumed at its first effective collision. A later shell can pass through a cell destroyed by an earlier shell, including in the same fan. Steel protects both sides, so Guardian cannot shoot through a shelter.

Both tactics are approved: reposition to a flank and trade HP for a fast clear, or open a firing line and alternate shots with retreats into permanent central cover. Very close approaches to the gun mouths are dangerous and unnecessary. Use the wider middle court for the shelter rhythm.

Pause, confirmed restart, level exit, live English/繁體中文, mute and reduced motion remain available. Sound starts muted. Short landscape screens scroll. The original range, Breakthrough, Colossus and Interception remain independently selectable. This build adds no tank roster, unlocks or campaign progression.

This is a creative-review build for **Confirm & Close**, not a deployment/publication. Physical-phone, independent first-time-player, other-engine and human assistive-technology testing were not performed. Automated accessibility checks do not establish full canvas/contrast accessibility. Existing production-licensing caveats and pending original M3-reference archival remain disclosed in provenance/QA.

繁體中文：選擇「圍城・第四關」開始。方向鍵或WASD移動，空白鍵開火；觸控可同時按住方向與「開火」。命中砲壘八次即可獲勝。守護者有三點生命，受傷後保護三秒。注意屋頂砲口的預備提示；五發扇形砲彈在發射後不會追蹤。磚牆可擋敵我一擊，鋼牆不會損壞。可積極進攻、以生命換速度，或射擊後退回中央永久掩護。沒有時限，可暫停、重試、離開、切換語言、靜音及減少動態效果。
