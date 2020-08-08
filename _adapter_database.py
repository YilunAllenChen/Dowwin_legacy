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


class db():

    def __init__(self, database='Dowwin'):
        '''
        Create a generic database connection with no specific collection.

        :param database: the database to connect to.
        '''
        self.db = client[database]
        self.coll = None
        self.test_connection()

    def update(self, doc, by) -> None:
        '''
        Generic update function.
        
        :param doc: The doc to replace with.
        :param by: The field used as key to replace the document. Function will attempt to find the document with the same 'by' field in the database and replace it with the one passed in.
        '''
        if doc is None or by is None:
            raise RuntimeError("Neither 'doc' nor 'by' can be None")
        self.coll.replace_one({by: doc[by]}, doc, True)

    def count(self) -> int:
        '''
        Generic count function to count how many documents are there in the collection.
        '''
        if self.coll is None:
            raise ConnectionError("No collection connected.")
        return self.coll.find().count()

    def delete(self, key, val) -> None:
        '''
        Generic delete function to delete one function that matches that has 'key' field equals to 'val'.
        
        :param key: The name of field that we need to check against
        :param val: The value of the field that we need to check against
        '''
        if key is None:
            raise RuntimeError("Key can't be None.")
        self.coll.delete_one({key: val})

    def test_connection(self) -> None:
        '''
        Generic function to test connection to the database.
        '''
        try:
            self.db['test'].insert_one({"test": 'test'})
            self.db.drop_collection('test')
        except:
            log("Unable to connect to database", 'error')
            raise ConnectionError("Unable to connect to the database")

    def get_image(self) -> list:
        found = self.coll.find()
        return [item for item in found]

class Market_Adapter(db):
    def __init__(self, database='Dowwin'):
        '''
        An adapter for the market collection.

        :param database: the database to connect to.
        '''
        super().__init__(database=database)
        self.coll = self.db['market']

    def get_symbols_to_update(self) -> list:
        '''
        Custom function to get the list of symbols to update in the market database.
        Symbols are sorted by their last update time so the one that's the most out of date will come first.
        '''
        data = self.coll.find().sort('lastUpdate')
        return [item['Symb'] for item in data]

    def get(self, symb) -> dict:
        '''
        market adapter custom get function to get the information about a stock.
        
        :param symb: the stock symbol (example: Microsoft -> MSFT).
        '''
        try:
            if type(symb) == list:
                all_data = self.coll.find({'Symb': {'$in': symb}})
                res = {}
                for data in all_data:
                    res[data.get('Symb')] = data.get('Info', {})
                return res
            data = self.coll.find_one({'Symb': symb})
            return data['Info'] if data is not None else None
        except Exception as e:
            print("Error getting info. ", e)
            raise e


class Bots_Adapter(db):

    def __init__(self, database='Dowwin'):
        '''
        An adapter for the bots database.
        
        :param database: The database to connect to.
        '''
        super().__init__(database=database)
        self.coll = self.db['tradebots']

    def filteredGet(self, query) -> list:
        '''
        Customized get function with a query filter

        :param query: The query
        '''
        found = self.coll.find(query)
        return [item for item in found]
    
    def get(self, sort=(None,None), num=100) -> list:
        '''
        Customized get function to get a certain number of bots.

        :param num: number of bots to get
        :param sort: tuple in form of (sort_by, order) where ascending is 1 and descending is -1.
        '''
        # Returns the bots that haven't been updated for longest.
        found = self.coll.find()

        if sort != (None, None):
            found = found.sort(sort[0], sort[1])
        found = found.limit(num)
        return [item for item in found]

    def get_sorted_by_next_update(self, num=100) -> list:
        '''
        Customized get function to sort by next update date.

        :param num: number of bots to get.
        '''
        return self.coll.find().limit(num).sort('nextUpdate')
    
db_market = Market_Adapter()
db_bots = Bots_Adapter()