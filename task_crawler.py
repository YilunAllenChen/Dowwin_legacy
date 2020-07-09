import yfinance as yf
import pymongo
import asyncio
from time import sleep
from datetime import datetime as dt
from _static_data import stock_symbols
from _global_config import DB_HOST
from _database_adapter import db_market
from __log import log


txt_log = open('crawler_logs/{}.txt'.format(str(dt.now())), 'w+')


async def task_crawler(loop, stop):
    log('*** Crawler Starting ***','ok')
    while not stop.is_set():
        for symb in stock_symbols:
            if stop.is_set():
                break
            try:
                ticker = yf.Ticker(symb)
                data = {
                    'Symb': symb,
                    'Info': ticker.get_info(),
                    'lastUpdate': dt.now()
                }
                db_market.update(data,by='Symb')
                txt_log.write('[{}] Data acquired for {}\n'.format(dt.now(), symb))
            except Exception as e:
                txt_log.write('[{}] Error occured when parsing {},{}\n'.format(
                    dt.now(), symb, e))
                log('Error occured parsing {}: {}'.format(symb, e),'error')
            await asyncio.sleep(1.5)
    log('*** Crawler shutting down ***','ok')