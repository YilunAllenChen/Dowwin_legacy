import pymongo
from time import time as now
HOST = "mongodb://localhost:27017/"

ONEDAY = 86400


class db():

    def __init__(self, host=HOST, database='Dowwin'):
        self.db = pymongo.MongoClient(host)[database]
        self.coll = None
    def update(self,doc,by):
        if doc is None or by is None:
            raise RuntimeError("Neither 'doc' nor 'by' can be None")
        self.coll.replace_one({by:doc[by]},doc, True)

class Market_Adapter(db):
    def __init__(self, host=HOST, database='Dowwin'):
        super().__init__(host=host, database=database)
        self.coll = self.db['market']

    def get(self, symb):
        try:
            data = self.coll.find_one({'Symb': symb})
            return data['Info'] if data is not None else None
        except Exception as e:
            print("Error getting info. ", e)
            raise e


class Bots_Adapter(db):
    def __init__(self, host=HOST, database='Dowwin'):
        super().__init__(host=host, database=database)
        self.coll = self.db['tradebots']

    def get(self, num=1, time=ONEDAY):
        # Only get robots that haven't been updated for a day.
        time_bar = now() - time
        print(time_bar)

        # Query looks for bots with lastUpdate timestamp before the bar or doesn't have the field (probably due to inactivity/deprecation)
        query = {
            '$or':[{
                'lastUpdate':{
                    '$lt': time_bar 
                }
            },{
                'lastUpdate':{
                    '$exists': False
                }
            }]
        }
        found = self.coll.find(query).limit(num)
        
        # Query used to update the timestamp for all bots found immediately to prevent other trainers do conflict trainings.
        # updated_timestamp = {
        #     '$set':{
        #         'lastUpdate': now()
        #     }
        # }
        # self.coll.update_many(query,updated_timestamp)

        return [item for item in found]



