import yfinance as yf
from static_data import SP500
from time import sleep
from datetime import datetime as dt
import pymongo


from global_config import DB_HOST
market = pymongo.MongoClient(DB_HOST)['Dowwin']['market']

log = open('crawler_logs/{}.txt'.format(str(dt.now())), 'w+')

try:
    while(True):
        for symb in SP500:
            try:
                ticker = yf.Ticker(symb)
                data = {
                    'Symb': symb,
                    'Info': ticker.get_info()
                }
                market.replace_one({'Symb': symb}, data, True)
                log.write('[{}] Data acquired for {}\n'.format(dt.now(), symb))
            except Exception as e:
                log.write('[{}] Error occured when parsing {},{}\n'.format(
                    dt.now(), symb, e))
            sleep(3)
except KeyboardInterrupt as k:
    print(" Keyboard Interrupt Detected. Cleaning Up...")
    log.close()
    exit()
