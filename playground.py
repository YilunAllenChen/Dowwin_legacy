from config import db_bots, db_market

for bot in db_bots.find():
    buy, sell = 0,0
    ops = bot['history']['operations']
    for op in ops:
        if op[1] > 0:
            buy += 1
        else:
            sell += 1
    print(bot['name'],'  :  ',buy,'buys and',sell,'sells')