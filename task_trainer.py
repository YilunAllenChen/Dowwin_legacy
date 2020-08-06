#
# Darwin Robotics, 2020
#

'''
This module defines a trainer task to train tradebots.
'''

from _Trader import Tradebot
from _database_adapter import db_bots
from __log import log
from time import sleep
import asyncio


async def task_trainer(loop, stop):
    log('*** Trainer Starting ***', 'ok')
    while not stop.is_set():
        for item in db_bots.get_sorted_by_next_update(1):
            if stop.is_set():
                break
            bot = Tradebot(data=item)
            bot.operate(autosave=True)
        await asyncio.wait({asyncio.sleep(1), stop.wait()}, return_when=asyncio.FIRST_COMPLETED)
    log('*** Trainer is shutting down ***', 'ok')
