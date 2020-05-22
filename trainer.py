from tradebot import Bot
from crawlbot import downloadData
from config import db_bots, forestSize
import sys



# downloadData(8,way='db')

# while db_bots.count_documents({}) < forestSize:
#     bot = Bot()
#     bot.save()

# allBots = db_bots.find()

# for epoch in db_bots.find():
#     bot = Bot(epoch)
#     bot.operate(way='db')