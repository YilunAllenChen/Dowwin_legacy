from _Trader import Tradebot
from _database_adapter import db_bots
from __log import log
from time import sleep
import asyncio


async def task_trainer(loop, stop, debug=False):
    log('*** Trainer Starting ***', 'ok')
    while not stop.is_set():
        vals = []
        for item in db_bots.get(20):
            if stop.is_set():
                break
            bot = Tradebot(data=item)
            bot.operate(autosave=True)
            vals.append(bot.evaluatePortfolio())
        if debug:
            log("Trainer: Finished training with a batch. \nHighest: {}\nLowest: {}\n Mean: {}\nStarting with a new batch.".format(
                max(vals), min(vals), sum(vals)/len(vals)), 'ok')
        await asyncio.wait({asyncio.sleep(600), stop.wait()}, return_when=asyncio.FIRST_COMPLETED)
    log('*** Trainer is shutting down ***', 'ok')
