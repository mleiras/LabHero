# /// script
# dependencies = [
#   "pygame_menu",
#   "pytmx",
# ]
# ///

import asyncio
import sys

print(f"[main.py] starting on {sys.platform} python {sys.version}", flush=True)

import LabHero

print("[main.py] LabHero imported, running main()", flush=True)

asyncio.run(LabHero.main())
