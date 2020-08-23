#
# Darwin Robotics, 2020
#

'''
This module provides utilities to interact with the database

'''

import pymongo
from time import time as now
from os import system
from __log import log, vlog
from _global_config import DB_HOST
from _static_data import stock_symbols


client = pymongo.MongoClient(host=DB_HOST)
try:
    client['Dowwin']['test'].insert_one({"test": 'test'})
    client['Dowwin'].drop_collection('test')
except:
    log("Unable to connect to database", 'error')
    raise ConnectionError("Unable to connect to the database")


_db_market = client['Dowwin']['market']
_db_bots = client['Dowwin']['tradebots']
_db_logs = client['Dowwin']['logs']

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                                    LOGGING
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def sync_upload_log(filepath)-> None:
    with open(filepath) as f:
        _db_logs.insert_one({str(now()): f.readlines()})

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                                    Bot
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def sync_update_bot(doc, by) -> None:
    '''
    Generic update function.
    
    :param doc: The doc to replace with.
    :param by: The field used as key to replace the document. Function will attempt to find the document with the same 'by' field in the database and replace it with the one passed in.
    '''
    if doc is None or by is None:
        raise RuntimeError("Neither 'doc' nor 'by' can be None")
    _db_bots.replace_one({by: doc[by]}, doc, True)

def sync_delete_bot(key, val) -> None:
    '''
    Generic delete function to delete one function that matches that has 'key' field equals to 'val'.
    
    :param key: The name of field that we need to check against
    :param val: The value of the field that we need to check against
    '''
    if key is None:
        raise RuntimeError("Key can't be None.")
    _db_bots.delete_one({key: val})

def sync_count_bots() -> int:
    return _db_bots.find().count()

def sync_get_bots_sorted_by_next_update(num=100) -> list:
    return _db_bots.find().limit(num).sort('nextUpdate')

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                                    MARKET
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def sync_get_market_image_minimal():
    '''
    Blocking function that gets the minimal image of the market database.
    '''
    cursor = _db_market.find({}, {'Symb':1, '_id': 0, 'Info': 1})
    return [item for item in cursor]
    
def sync_get_stock(symb):
    return _db_market.find_one({'Symb': symb})['Info']