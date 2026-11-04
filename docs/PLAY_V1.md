# Armorheart v1.0 release candidate

Extract `Armorheart-v1.0-RC.zip` and open `Armorheart-v1.0-RC/index.html`. The single HTML embeds the entire game, artwork and styles. If the browser restricts local files, run this command from the extracted `Armorheart-v1.0-RC` folder:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080/`. No installation, account or runtime network connection is needed after the document loads. Local HTTP with all subsequent requests blocked is verified; direct `file://` opening remains unverified in this managed browser.

## Four missions, any order

All four missions are available immediately and remain replayable. Select a mission, then Start. The training range is separate and grants no campaign rewards.

- **Breakthrough:** destroy individual brick cells to open a physically viable evacuation route. Steel stays. The transport departs automatically when a full route exists. Ninety-second deadline; two-shot longer bypass or four-shot shorter shortcut.
- **Colossus:** defeat the four-HP gorilla during grounded pauses. Observe the five-stop jump pattern. The tank has three HP and three-second protection after damage; no mission timer.
- **Interception:** hit the six-HP battleship before it exits the clockwise peninsula route. Watch its fixed starboard three-shell volleys. The tank has three HP; no separate countdown.
- **Siege:** hit the eight-HP Fortress. Five-shell fans arrive every three seconds after a warning. Brick cover absorbs one effective hit; steel shelters remain. Aggressive HP trading and tactical shelter rhythms are both valid. Three tank HP, no timer.

## Your collection

T—01 Guardian is always available. The first, second and third **distinct mission victories** unlock T—02 Bulwark, T—03 Vanguard and T—04 Sentinel respectively, regardless of mission order. Replaying a cleared mission earns no additional tank. Clear all four distinct missions to earn the **campaign commendation**, not a fifth tank.

The four original designs have **identical movement, protection, firepower, collision, recoil and muzzle positions**. Choose any unlocked tank in the selector before a new attempt. Unlocking a tank does not silently replace the one you chose. A selection applies to the next/new attempt; it never changes an active battle.

Victory offers **Next / Missions / Replay**. Next opens the next numbered mission, even if it was already cleared. Siege is the last numbered mission and offers Missions / Replay even when it is your first win. Navigation does not grant rewards. Failure offers Retry / Missions; retry resets only the current attempt and its cover.

Progress and selected tank stay in this browser on this device when local storage is permitted. Clearing browser data, changing origin/browser/device, private browsing or local-file restrictions can remove or isolate that progress. Storage failures leave the session playable with a visible notice. Malformed saves recover safely; unrecognized newer saves remain untouched and this version uses session-only progress. There is no cloud sync, account or data collection. Concurrent multi-tab save merging is not guaranteed.

## Controls and accessibility

Arrows or WASD move and face immediately. Hold Space to fire, once per second with unlimited ammunition. On touch, hold a direction and Fire simultaneously. Pause, confirmed restart and level exit are available; leaving an active attempt preserves earned campaign progress. Sound starts muted. Use the music-note button for mute, the motion button for reduced motion, and English/繁體中文 for live language switching. System reduced-motion preference also applies. Native buttons support keyboard focus/Enter; mission results announce through the existing live region.

Phone portrait is recommended. Narrow 320px layouts are checked; short landscape screens require scrolling. The Canvas battlefield still needs vision and rapid spatial input: automated audits and contrast checks are not full nonvisual accessibility certification.

繁體中文：四個任務一開始皆可選擇，順序不限。第一次完成不同任務，依序解鎖「壁壘」、「先鋒」、「哨衛」；重複勝利不重複發獎。完成四個不同任務可獲戰役嘉獎，沒有第五台戰車。四款外觀的移動、碰撞、生命與火力完全相同。方向鍵／WASD移動，空白鍵開火；觸控可同時按住方向與「開火」。可暫停、重試、離開、即時切換語言、靜音及減少動態效果。進度僅保存在允許儲存的本機瀏覽器；無法儲存時會提示，當次遊玩仍可解鎖。

This is the integrated **v1.0 RC1 for final Confirm & Close**, not an authorized public release. All four individual missions are creatively accepted; the composed game and new collection await final review. Physical-phone, independent first-time-player, other-browser-engine and human assistive-technology testing were not performed. Existing artwork licensing caveats remain; see the included provenance files. No blanket commercial redistribution rights are asserted.
