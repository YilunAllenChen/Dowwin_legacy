#
# Darwin Robotics, 2020
#

from _adapter_database_async import get_image
from _adapter_database import db_market
from __log import log, vlog, debug
import asyncio

market_cache = {}

async def task_cache_manager(stop):    
    log('*** Cache Manager Starting ***','ok')
    debug("Initializing cache...")
    init_cache = db_market.get_image()
    for item in init_cache:
            market_cache[item.get('Symb')] = item.get('Info')
    while not stop.is_set():
        result = await asyncio.create_task(get_image())
        for item in result:
            market_cache[item.get('Symb')] = item.get('Info')
        debug("Cache Updated")
        await asyncio.wait({asyncio.sleep(3600), stop.wait()}, return_when=asyncio.FIRST_COMPLETED)
    log("*** Cache Manager is shutting down ***",'ok')