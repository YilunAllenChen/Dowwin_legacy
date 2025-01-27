#
# Darwin Robotics, 2020
#

'''
This module finds stock symbols that are not in the database and fill them in.
'''


import asyncio
from datetime import datetime as dt
from _static_data import stock_symbols
from _adapter_database_async import async_get_all_symbols, async_update_stock
from _crawler_apis import Ticker
from __log import log, debug
from os import makedirs




async def task_scout(loop, stop):
    log('*** Scout Starting ***','ok')
    
    symbs = await async_get_all_symbols()

    for symb in stock_symbols:
        if stop.is_set():
            break
        try:
            if symb not in symbs:
                debug(f"Scout detected that {symb} is not in the database. Acquiring info now")
                ticker = Ticker(symb)
                await ticker.update()
                data = {
                        'Symb': symb,
                        'Info': ticker.info,
                        'Data': ticker.raw,
                        'lastUpdate': dt.now()
                }
                await async_update_stock(data,by='Symb')
                await asyncio.wait({asyncio.sleep(1.5),stop.wait()},return_when=asyncio.FIRST_COMPLETED)
        except Exception as e:
            log(f"Error parsing info for {symb} : {e}",'error')
    log('*** Scout shutting down ***','ok')
