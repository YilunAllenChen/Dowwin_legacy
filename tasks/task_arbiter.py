#
# Darwin Robotics, 2020
#

'''
This module fills the forest's empty slots with randomly generated new tradebots.
'''

from __log import log, debug
from _adapter_database import sync_count_bots
from _Trader import Tradebot
from GLOBAL_CONFIG import BOT_THRESHOLD
from time import sleep
import asyncio


async def task_arbiter(loop, stop):
    log('*** Arbiter Starting ***', 'ok')
    while not stop.is_set():
        # Add new bots until cap
        added = 0
        for _ in range(min([200, BOT_THRESHOLD - sync_count_bots()])):
            newbot = Tradebot()
            newbot.save()
            added += 1
        debug('Arbiter: Added {} new trade bots into the forest'.format(added))

        await asyncio.wait({asyncio.sleep(60), stop.wait()}, return_when=asyncio.FIRST_COMPLETED)
    log("*** Arbiter shutting down ***", 'ok')
 