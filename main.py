

# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import nest_asyncio

# 1) Ensure the 'src/' directory is on the import path
BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "src")
if os.path.isdir(SRC_DIR):
    sys.path.insert(0, os.path.abspath(SRC_DIR))

# 2) Import your project modules
from src import utility, globe

# 3) Patch the running event loop so asyncio.run() works under Spyder
nest_asyncio.apply()

async def main():
    # Initialize and enter your game loop
    utility.init_game()
    utility.game_loop()

if __name__ == "__main__":
    # Single entrypoint: run the async main()
    asyncio.run(main())
