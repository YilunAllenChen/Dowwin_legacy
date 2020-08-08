#
# Darwin Robotics, 2020
#

'''
This module provides utilities to interact with the database
'''

import asyncio
import motor.motor_asyncio
from __log import log, vlog
from _global_config import DB_HOST

client = motor.motor_asyncio.AsyncIOMotorClient(DB_HOST)

async_db_market = client['Dowwin']['market']
async_db_bot = client['Dowwin']['tradebots']

async def get_image():
    cursor = async_db_market.find()
    documents = await cursor.to_list(length=None)
    print(documents)
    return documents

async def get_market_image_minimal():
    cursor = async_db_market.find({},{'Info':1, "Symb": 1})
    documents = await cursor.to_list(length=None)
    print(documents)
    return documents

async def get_all_symbols():
    cursor = async_db_market.find({},{"Symb": 1})
    documents = await cursor.to_list(length=None)
    return [document['Symb'] for document in documents]




loop = asyncio.get_event_loop()
loop.run_until_complete(get_all_symbols())

