'''
This module acquires bots data from the database and perform numerous analysis.
'''


from config import db_bots, db_market
import sys
from datetime import datetime




# Function counts buys and sells in
def countBuysAndSells(query={}):
    buy, sell = 0, 0
    for bot in db_bots.find(query):
        ops = bot['history']['operations']
        for op in ops:
            if op[1] > 0:
                buy += 1
            else:
                sell += 1
    return buy, sell
# print(countBuysAndSells())

# Function returns a list of bots with evaluation above bar.


def filterByEvalutaion(bar=100000, query={}):
    res = []
    for bot in db_bots.find(query):
        hist = bot['history']['evaluation']
        if(len(hist) < 2):
            pass
        else:
            lastHist = hist[-1][1]
            if lastHist > bar:
                res.append(bot)
    return res


def printBuysAndSellsCounts(query={}):
    for bot in db_bots.find(query):
        buy, sell = 0, 0
        ops = bot['history']['operations']
        for op in ops:
            if op[1] > 0:
                buy += 1
            else:
                sell += 1
        print(bot['id'], bot['name'], '  :  ', buy, 'buys and', sell, 'sells')


def printGoodAndBad(query={}):
    good, bad, better = 0, 0, 0
    for bot in db_bots.find(query):
        hist = bot['history']['evaluation']
        if(len(hist) < 2):
            pass
        else:
            lastHist = hist[-1][1]
            secLastHist = hist[-2][1]
            good += 1 if lastHist > 100000 else 0
            bad += 1 if lastHist < 100000 else 0
            better += 1 if lastHist > secLastHist else 0
    print("among 2000 robots,", good, 'are winning,',
          bad, 'are losing', better, 'are improving')


def printHist(query={}):
    bot = db_bots.find_one(query)
    recents, recents_str = bot['history']['operations'], ''
    [timestamp, shares, symb, opPrice, cash] = [0, 0, 0, 0, 0]
    for each in recents:
        [timestamp, shares, symb, opPrice, cash] = each
        date = datetime.fromtimestamp(timestamp/1000).date()
        shares = int(shares)
        avgCost = (bot['portfolio'][each[2]]['avgcost'])
        gain = -int(shares)*round((opPrice-avgCost),3)
        if shares < 0:
            recents_str += '\n' + \
                "{4} \033[91m Selled \033[00m {0} shares of {1} at {2}. Gain: {3}".format(
                    -int(shares), symb, opPrice, gain, date)
        else:
            recents_str += '\n' + \
                "{3} \033[92m Buyed \033[00m {0} shares of {1} at {2}.".format(
                    int(shares), symb, opPrice, date)
    recents_str += '\r'
    print("ID: {0} Name: {1}{2} Value: {3}".format(
        bot['id'] % 100000, bot['name'], (30-len(bot['name'])) *
        ' ', bot['history']['evaluation'][-1][1]
    ))
    print(recents_str)


def winners_stats(bar=100000):
    winners = filterByEvalutaion(bar=bar)
    avgGainRate = sum([winner['history']['evaluation'][-1][1]/100000 for winner in winners]) / len(winners)
    print("Average Gain Rate for the winners: {0}".format(avgGainRate))




res = filterByEvalutaion(bar=108000)
for bot in res:
    print(bot['chars'], bot['history']['evaluation'][-1][-1])
    printBuysAndSellsCounts(query={'_id': bot['_id']})

printGoodAndBad()

winners_stats(bar=108000)

