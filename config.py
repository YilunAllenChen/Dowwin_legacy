# pymongo provides APIs to interact with MongoDB database
import pymongo

database = pymongo.MongoClient(
    "mongodb://localhost:27017/")["Dowwin"]

market = database['market']
bots = database['tradebots']