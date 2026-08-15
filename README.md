# Random Walk 🐿️ on a lonely island

I need to add visuals!

A happy squirrel jumping around alone on a lonely island! This is a simulation of a random walk in 1D. Originally designed to be employed as a learning aid (interactive tool), for students of basic university statistics.

Contributions and any feedback are welcome, although the work on this is finished.

## Running locally (desktop)

```sh
pip install -r requirements.txt
python main.py
```

## Web build (GitHub Pages)

The game is deployed to GitHub Pages from the `web/` folder. Rebuild the
pygbag bundle with:

```sh
pygbag --build --ume_block 1 .
```

then copy `build/web/assets.apk` and `build/web/assets.tar.gz` into `web/`
(keep the existing `web/index.html`). Push to deploy.

Notes for the pygbag 0.9.x build:

- The `pygame_gui/` and `i18n/` packages are vendored inside the game folder
  so nothing is pip-installed at runtime (pygbag 0.9.3 does not bundle
  third-party packages, and PyPI has no `i18n` project).
- The PEP 723 block must not pin versions (pins crash the runtime's
  `find_spec`), and `import pygame` must appear in `main.py` so the runtime
  preloads the pygame submodules.
- pygame_gui is patched for wasm: no loading threads (Emscripten cannot start
  threads) and fonts are loaded from a filesystem path instead of a BytesIO
  (pygame-ce wasm `pgRWops_FromObject` only accepts paths).
