'''
This module is a high-level interface of the system.
'''



from crawlbot import downloadData
from time import sleep
from tradebot import Bot
from config import db_bots, forestSize
from SymbList import SP500


# downloadData(8,way='db')

print("Download complete. Now starting to train.")



# Fill up the forest with new bots
while db_bots.count_documents({}) < forestSize:
    bot = Bot()
    bot.save()

allBots = db_bots.find()
sleep(0.5)
for epoch in db_bots.find():
    bot = Bot(epoch)
    bot.operate(way='db')
    bot.eliminate(way='db',bar=98000)

