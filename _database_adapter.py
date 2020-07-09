import pymongo
from time import time as now
from os import system
from __log import log
from _global_config import DB_HOST


client = pymongo.MongoClient(host=DB_HOST)

class db():

    def __init__(self, database='Dowwin'):
        self.db = client[database]
        self.coll = None
        self.test_connection()

    def update(self,doc,by):
        if doc is None or by is None:
            raise RuntimeError("Neither 'doc' nor 'by' can be None")
        self.coll.replace_one({by:doc[by]},doc, True)
    
    def count(self):
        return self.coll.find().count()

    def delete(self,key,val):
        if key is None:
            raise RuntimeError("Key can't be None.")
        self.coll.delete_one({key:val})
    
    def test_connection(self):
        try:
            self.db['test'].insert_one({"test":'test'})
            self.db.drop_collection('test')
        except:
            log("Unable to connect to database",'error')
            raise

class Market_Adapter(db):
    def __init__(self, database='Dowwin'):
        super().__init__(database=database)
        self.coll = self.db['market']

    def get(self, symb):
        try:
            data = self.coll.find_one({'Symb': symb})
            return data['Info'] if data is not None else None
        except Exception as e:
            print("Error getting info. ", e)
            raise e


class Bots_Adapter(db):
    def __init__(self, database='Dowwin'):
        super().__init__(database=database)
        self.coll = self.db['tradebots']

    def get(self, num=100):
        # Returns the bots that haven't been updated for longest.
        found = self.coll.find().sort('nextUpdate').limit(num)
        return [item for item in found]

db_market = Market_Adapter()
db_bots = Bots_Adapter()