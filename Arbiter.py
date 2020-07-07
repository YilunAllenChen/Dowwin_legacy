from database_adapter import db_bots
from Trader import Tradebot
from log import *
from global_config import BOT_THRESHOLD
from time import sleep
import asyncio

async def Arbiter(loop, stop):
    log('*** Arbiter Starting ***','ok')
    while not stop.is_set():
        # Add new bots until cap
        added = 0
        for _ in range(BOT_THRESHOLD - db_bots.count()):
            newbot = Tradebot()
            newbot.save()
            added += 1
        log('Arbiter: Added {} new trade bots into the forest'.format(added))

        await asyncio.sleep(1)
    log("*** Arbiter shutting down ***",'ok')