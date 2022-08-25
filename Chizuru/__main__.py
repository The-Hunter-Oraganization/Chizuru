import glob
from pathlib import Path
import logging
from Chizuru import pbot
import random
import asyncio

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


pbot.start()
loop = asyncio.get_event_loop()
loop.run_forever()    