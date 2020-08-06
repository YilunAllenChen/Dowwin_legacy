#
# Darwin Robotics, 2020
#

'''
This module finds stock symbols that are not in the database and fill them in.
'''


import asyncio
from datetime import datetime as dt
from _static_data import stock_symbols
from _database_adapter import db_market
from _crawler_apis import Ticker
from __log import log, debug
from os import makedirs




async def task_scout(loop, stop):
    log('*** Scout Starting ***','ok')
    
    symbs = db_market.get_symbols_to_update()

    for symb in stock_symbols:
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
                db_market.update(data,by='Symb')
                await asyncio.wait({asyncio.sleep(1.5),stop.wait()},return_when=asyncio.FIRST_COMPLETED)
        except Exception as e:
            log(f"Error parsing info for {symb} : {e}",'error')
    log('*** Scout shutting down ***','ok')
