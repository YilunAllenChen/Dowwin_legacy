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

async def get_image():
    cursor = async_db_market.find()
    documents = await cursor.to_list(length=None)
    return [document for document in documents]


