import yfinance as yf
from static_data import stock_symbols
from time import sleep
from datetime import datetime as dt
import pymongo
from global_config import DB_HOST
market = pymongo.MongoClient(DB_HOST)['Dowwin']['market']
from log import log
import asyncio


txt_log = open('crawler_logs/{}.txt'.format(str(dt.now())), 'w+')


async def Courier(loop, stop):
    log('*** Courier Starting ***','ok')
    while not stop.is_set():
        for symb in stock_symbols:
            if stop.is_set():
                break
            try:
                ticker = yf.Ticker(symb)
                data = {
                    'Symb': symb,
                    'Info': ticker.get_info()
                }
                market.replace_one({'Symb': symb}, data, True)
                txt_log.write('[{}] Data acquired for {}\n'.format(dt.now(), symb))
            except Exception as e:
                txt_log.write('[{}] Error occured when parsing {},{}\n'.format(
                    dt.now(), symb, e))
                log('Error occured parsing {}: {}'.format(symb, e),'error')
            await asyncio.sleep(1.5)
    log('*** Courier shutting down ***','ok')