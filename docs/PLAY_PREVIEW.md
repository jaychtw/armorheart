# Play the Guardian POC

1. Download `Armorheart-Guardian-POC.zip` from the repository's `artifacts` folder and extract it.
2. Open `Guardian-POC/guardian.html` in a modern desktop browser. Everything is embedded; no npm packages or network services are needed by the game.
3. Choose **Enter the range**. Use arrow keys or WASD to move and hold Space to fire. On touch, hold a direction and Fire together. Clear the six brick blocks; steel barriers remain.

If your browser blocks opening local HTML files, open a terminal in the extracted `Guardian-POC` folder and run:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

On Windows, use `py -m http.server 8080 --bind 127.0.0.1` if `python3` is unavailable. Then visit `http://localhost:8080/guardian.html`.

The self-contained preview was tested over local HTTP with every additional request blocked. Direct `file://` opening was not verified because the managed test browser blocks it. No public deployment is required.

This is the bounded Guardian technical prototype, not the full game or accepted production art. The included provenance record identifies remaining licensing concerns. The full editable source, tests, screenshots and recoil recording remain in the GitHub repository.
