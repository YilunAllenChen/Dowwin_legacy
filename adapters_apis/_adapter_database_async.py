#
# Darwin Robotics, 2020
#

'''
This module provides async-compatible utilities to interact with the database.
'''

import asyncio
import motor.motor_asyncio
from __log import log, vlog
from GLOBAL_CONFIG import DB_HOST

client = motor.motor_asyncio.AsyncIOMotorClient(DB_HOST)
_db_market = client['Dowwin']['market']
_db_bot = client['Dowwin']['tradebots']

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                                    MARKET
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
async def async_get_market_image_minimal() -> list:
    '''
    Obtain a minimal image of the market collection.
    '''
    cursor = _db_market.find({},{'Info':1, "Symb": 1})
    documents = await cursor.to_list(length=None)
    return documents

async def async_get_all_symbols() -> list:
    '''
    Custom function to get the list of symbols to update in the market database.
    Symbols are sorted by their last update time so the one that's the most out of date will come first.
    '''
    cursor = _db_market.find({},{"Symb": 1})
    documents = await cursor.to_list(length=None)
    return [document['Symb'] for document in documents]

async def async_update_stock(stock: dict, by: str) -> None:
    '''
    Function to update a stock.

    :param stock: The stock data
    :param by: Update the stock data with the same field as {by}.
    '''
    result = await _db_market.update_one({by: stock.get(by)}, {'$set':stock}, True)
    return result

async def async_get_stock(symb: str) -> dict:
    '''
    async market adapter custom get function to get the information about a stock.
    
    :param symb: the stock symbol (example: Microsoft -> MSFT).
    '''
    try:
        return await _db_market.find_one({'Symb': symb})
    except Exception as e:
        print("Error getting info. ", e)
        raise e



# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_all_symbols())

