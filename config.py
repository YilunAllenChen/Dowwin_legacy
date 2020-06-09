# pymongo provides APIs to interact with MongoDB database
import pymongo


database = pymongo.MongoClient(
    "mongodb://localhost:27017/")["Dowwin"]
db_market = database['market']
db_bots = database['tradebots']


forestSize = 2000