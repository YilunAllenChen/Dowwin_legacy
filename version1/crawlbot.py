'''
Working multi-threaded crawlbot that downloads data from yfinance interface.
'''



import yfinance as yf
import threading
import sys
import pandas as pd
import numpy as np
from json import dumps
from time import sleep
from config import db_market
from SymbList import SP500
lock = threading.Lock()

total = len(SP500)
count = 0

def processHist(ticker:yf.Ticker):
    hist = {}
    info = {}
    data = ticker.history(period='max',interval='5d')
    data = data.where(pd.notnull(data),None)
    try:
        for item in data.T.iteritems():
            stuff = dict(item[1])
            try:
                hist[item[0].value] = stuff
            except Exception as e:
                hist[item[0]] = stuff
    except Exception as e:
        hist['error'] = e
    return hist

def get_next_symb():
    lock.acquire()
    res = SP500.pop() if len(SP500) != 0 else None
    lock.release()
    return res

def threaded_download_single(thread_id, way='fs'):
    this = threading.current_thread()
    this.alive = True
    while(True):
        sleep(1.5)
        symb = get_next_symb()
        if symb is None or not this.alive:
            break
        else:
            ticker = yf.Ticker(symb)
            try:
                data = {
                    # TODO: Hist gives error because int cannot be key of mongodb doc. Fix this.
                    # "Hist": processHist(ticker)
                    "Symb": symb,
                    "Info": ticker.get_info(),
                }
                if way=='fs':
                    f = open(('dataset_static/'+symb+'.json'), 'w')
                    f.write(dumps(data))
                    f.close()
                elif way == 'db':
                    db_market.replace_one({'Symb': data['Symb']}, data, True)
            except Exception as e:
                print('Failed to fetch data for',symb,': ',e)
            global count
            count += 1
            
            sys.stdout.write('\r[{0}] {2} / {3} ({1}%)'.format('#'*int(count/total*20)+' '*(
                20-int(count/total*20)), int(count/total*100), count, total))
            sys.stdout.flush()
    this.alive = False


def downloadData(num_thread=8, way='fs'):
    threads = []
    for i in range(num_thread):
        newTD = threading.Thread(target=threaded_download_single, args=(i,way))
        newTD.daemon=True
        threads.append(newTD)
    for thread in threads:
        thread.start()
    try:
        running = True
        while(running):
            running = False
            for thread in threads:
                if thread.alive:
                    running = True
                thread.join(0.5)
    except KeyboardInterrupt as e:
        for thread in threads:
            thread.alive = False
            thread.join()
        sys.exit(e)