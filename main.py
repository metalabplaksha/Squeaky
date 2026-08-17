# Web (pygbag) entry point for Squeaky.
# Notes:
# - `import pygame` here is required: it makes the pygbag 0.9.x runtime preload
#   and patch the pygame submodules (otherwise pygame.surface is missing at
#   runtime and pygame_gui fails to import).
# - The PEP 723 block is fully commented out: version pins crash the runtime's
#   find_spec, and with pygame_gui + i18n vendored in this folder nothing needs
#   to be pip-installed at runtime.
# - The desktop main.py (repo root) uses nest_asyncio/asyncio.run; on wasm we
#   just await the game loop, letting pygbag drive the asyncio event loop.
#
# /// script
# dependencies = []
# ///
import sys
import asyncio

import pygame

from src import utility


async def main():
    utility.init_game()
    await utility.game_loop()


if __name__ == "__main__":
    asyncio.run(main())