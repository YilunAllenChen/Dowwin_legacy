from Trader import Tradebot
from database_adapter import db_bots
from log import *
from time import sleep
import asyncio


async def Trainer(loop, stop): 
    log('*** Trainer Starting ***','ok')
    while not stop.is_set():
        vals = []
        for item in db_bots.get(200):
            if stop.is_set():
                break
            bot = Tradebot(data=item)
            bot.operate(autosave=True)
            vals.append(bot.evaluatePortfolio())
        log("Trainer: Finished training with a batch. \nHighest: {}\nLowest: {}\n Mean: {}\nStarting with a new batch.".format(max(vals),min(vals),sum(vals)/len(vals)),'ok')
        await asyncio.sleep(1)
    log('*** Trainer is shutting down ***','ok')