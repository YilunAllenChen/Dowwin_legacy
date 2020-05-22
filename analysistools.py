from config import db_bots, db_market



def buysAndSells(query={}):
    for bot in db_bots.find(query):
        buy, sell = 0, 0
        ops = bot['history']['operations']
        for op in ops:
            if op[1] > 0:
                buy += 1
            else:
                sell += 1
        print(bot['name'], '  :  ', buy, 'buys and', sell, 'sells')
    return


def goodAndBad(query={}):
    good, bad, better = 0, 0, 0
    for bot in db_bots.find(query):
        hist = bot['history']['evaluation']

        if(len(hist) < 2):
            pass
        else:
            lastHist = hist[-1][1]
            secLastHist = hist[-2][1]
            good += 1 if lastHist > 100000 else 0
            bad += 1 if lastHist < 98000 else 0
            better += 1 if lastHist > secLastHist else 0
    print("among 2000 robots,",good,'are winning,',bad,'are losing',better,'are improving')


goodAndBad()
