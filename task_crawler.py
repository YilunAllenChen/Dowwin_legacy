#
# Darwin Robotics, 2020
#

'''
This module defines a task to constantly update the database with the APIs provided by crawler_apis
'''

import asyncio
from datetime import datetime as dt
from _crawler_apis import Ticker
from _adapter_database import db_market
from _adapter_database_async import get_all_symbols
from __log import log, debug
from os import makedirs


makedirs('crawler_logs', exist_ok=True)
txt_log = open('./crawler_logs/{}.txt'.format(str(dt.now().timestamp())), 'w+')


async def task_crawler(loop, stop):
    log('*** Crawler Starting ***','ok')
    while not stop.is_set():
        symbs = await asyncio.create_task(get_all_symbols())
        debug("Done")
        for symb in symbs:
            if stop.is_set():
                break
            try:
                debug("Updating symb " + symb)
                ticker = Ticker(symb)
                await ticker.update()
                debug("Update complete")
                data = {
                    'Symb': symb,
                    'Info': ticker.info,
                    'Data': ticker.raw,
                    'lastUpdate': dt.now()
                }
                db_market.update(data,by='Symb')
                debug(f'[{dt.now()}] Data acquired for {symb}\n')
            except Exception as e:
                debug(f'[{dt.now()}] Error occured when parsing {symb},{e}\n')
                log('Error occured parsing {}: {}'.format(symb, e),'error')
            await asyncio.wait({asyncio.sleep(1.5),stop.wait()},return_when=asyncio.FIRST_COMPLETED)
    log('*** Crawler shutting down ***','ok')
