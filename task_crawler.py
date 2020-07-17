import pymongo
import asyncio
from time import sleep
from datetime import datetime as dt
from _static_data import stock_symbols
from _global_config import DB_HOST
from _crawler_apis import Ticker
from _database_adapter import db_market
from __log import log


txt_log = open('./crawler_logs/{}.txt'.format(str(dt.now().timestamp())), 'w+')


async def task_crawler(loop, stop, debug=False):
    log('*** Crawler Starting ***','ok')
    while not stop.is_set():
        symbs = db_market.get_symbols_to_update()
        for symb in symbs:
            if stop.is_set():
                break
            try:
                ticker = Ticker(symb)
                await ticker.update()
                data = {
                    'Symb': symb,
                    'Info': ticker.info,
                    'Data': ticker.raw,
                    'lastUpdate': dt.now()
                }
                db_market.update(data,by='Symb')
                txt_log.write('[{}] Data acquired for {}\n'.format(dt.now(), symb))
            except Exception as e:
                txt_log.write('[{}] Error occured when parsing {},{}\n'.format(
                    dt.now(), symb, e))
                log('Error occured parsing {}: {}'.format(symb, e),'error')
            await asyncio.wait({asyncio.sleep(1.5),stop.wait()},return_when=asyncio.FIRST_COMPLETED)
    log('*** Crawler shutting down ***','ok')
