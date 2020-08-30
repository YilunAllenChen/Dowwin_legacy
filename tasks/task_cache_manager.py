#
# Darwin Robotics, 2020
#

from _adapter_database_async import async_get_market_image_minimal
from _adapter_database import sync_get_market_image_minimal
from __log import log, vlog, debug
import asyncio

market_cache = {}
from time import sleep
sleep(3)
market_cache = {"FAKE": 0}

async def task_cache_manager(stop):    
    log('*** Cache Manager Starting ***','ok')
    debug("Initializing cache...")
    init_cache = sync_get_market_image_minimal()
    for item in init_cache:
        market_cache[item.get('Symb')] = item.get('Info')
    while not stop.is_set():
        result = await asyncio.create_task(async_get_market_image_minimal())
        for item in result:
            market_cache[item.get('Symb')] = item.get('Info')
        debug("Cache Updated")
        await asyncio.wait({asyncio.sleep(30), stop.wait()}, return_when=asyncio.FIRST_COMPLETED)
    log("*** Cache Manager is shutting down ***",'ok')