#
# Darwin Robotics, 2020
#

'''
This module defines a task to constantly update the database with the APIs provided by crawler_apis
'''

import asyncio
from datetime import datetime as dt
from _crawler_apis import Ticker
from _adapter_database_async import async_get_all_symbols, async_update_stock
from __log import log, debug
from os import makedirs


makedirs('crawler_logs', exist_ok=True)
txt_log = open('./crawler_logs/{}.txt'.format(str(dt.now().timestamp())), 'w+')


async def task_crawler(loop, stop):
    log('*** Crawler Starting ***','ok')
    while not stop.is_set():
        symbs = await asyncio.create_task(async_get_all_symbols())
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
                await async_update_stock(data, by='Symb')
                debug(f'[{dt.now()}] Data acquired for {symb}\n')
            except Exception as e:
                log(f'[{dt.now()}] Error occured when parsing {symb},{e}\n','error',to_file=True)
            await asyncio.wait({asyncio.sleep(1.5),stop.wait()},return_when=asyncio.FIRST_COMPLETED)
    log('*** Crawler shutting down ***','ok')
