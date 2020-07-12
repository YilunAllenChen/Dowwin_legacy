from math import log10
from random import choice, random
from time import time as now
from datetime import datetime, timedelta
from _names import names
from _database_adapter import db_bots, db_market
from _static_data import stock_symbols
from _global_config import ELIMINATION_THRESHOLD, STARTING_FUND
import asyncio

from __log import log


class Tradebot():
    def __init__(self, **kwargs):
        self.data = kwargs.get("data", {
            'id': now()*1000,
            'name': choice(names),
            'cash': STARTING_FUND,
            'value': STARTING_FUND,
            'portfolio': {},
            'activities': [],
            'evaluations': [],
            'chars': {
                'growth': random(),
                'value': random(),
                'profitmargin': random(),
                'stoplossmargin': random(),
                'activeness': int(random()*100),
                'operatinginterval': 2*int(random()*72) # in hours
            },
            'lastUpdate': datetime.now(),
        })
        if self.data.get('nextUpdate') is None:
            interval = timedelta(hours=self.data['chars']['operatinginterval'])
            self.data['nextUpdate'] = self.data['lastUpdate'] + interval

    def selfcheck(self):
        return True

    def save(self):
        db_bots.update(self.data,by='id')

    def buy(self, symb, shares):
        shares = int(shares)
        if shares <= 0:
            #print("Cannot buy less than or equal to 0 share")
            return
        stock = db_market.get(symb)
        if stock is None:
            log("Problem obtaining stock [{}]".format(symb),'error')
        if stock['ask'] <= 0.1:
            return

        trans = shares * stock['ask']
        if self.data['cash'] < trans:
            return
        try:
            pick = stock['symbol']
            if pick in self.data['portfolio']:
                position = self.data['portfolio'][pick]
                newAvgCost = (
                    position['avgcost'] * position['shares'] + trans) / (shares + position['shares'])
                position['avgcost'] = newAvgCost
                position['shares'] += shares
            else:
                self.data['portfolio'][pick] = {
                    'shares': shares, 'avgcost': stock['ask']}
            self.data['cash'] -= trans
        except Exception as e:
            print("Error buying, ", e)
            raise
        self.data['activities'].append(
            (datetime.now(), shares, symb, stock['ask'], self.data['cash']))

    # sell 'shares' number of a certain stock. Stock is of dict type containing information 'symbol', 'ask' and 'bid'.
    def sell(self, symb, shares):
        shares = int(shares)
        stock = db_market.get(symb)
        pick = symb
        if pick not in self.data['portfolio']:
            return
        sellshares = min([self.data['portfolio'][pick]['shares'], int(shares)])
        if sellshares <= 0:
            return
        if stock['bid'] <= 0.1:
            return

        try:
            self.data['cash'] += stock['bid'] * shares
            if self.data['portfolio'][pick]['shares'] == sellshares:
                self.data['portfolio'].pop(pick)
            else:
                self.data['portfolio'][pick]['shares'] -= shares
            self.data['activities'].append(
                (datetime.now(), -shares, symb, stock['bid'], self.data['cash']))
        except Exception as e:
            log("Error occured selling stock {}. Details: {}".format(symb, e))

    def evaluatePortfolio(self):
        evalutaion = self.data['cash']
        positions = self.data['portfolio'].items()
        for position in positions:
            price = db_market.get(position[0])['bid']
            if price < 0.1:
                continue
            else:
                evalutaion += price * position[1]['shares']
        return evalutaion

    # buyEvaluate computes how many shares of a stock should you buy (If negative then don't buy of course).
    # TODO: Develop a better evaluation algorithm.
    def buyEvaluate(self, symb):
        stock = db_market.get(symb)
        try:
            value = log10(stock['marketCap']) / stock['trailingPE']
            growth = 10 * stock['52WeekChange'] * \
                stock['beta'] + 10 * stock['earningsQuarterlyGrowth']
            return self.data['chars']['growth'] * growth + self.data['chars']['value'] * value
        except:
            return 0

    # sellEvaluate computes how many shares of a stock should you sell (If negative then don't sell of course).
    # TODO: Develop a better evaluation algorithm.
    def sellEvaluate(self, symb):
        stock = db_market.get(symb)
        try:
            return (stock['bid'] - self.data['portfolio'][symb]['avgcost']) * self.data['chars']['profitmargin']/stock['bid'] * self.data['portfolio'][symb]['shares']
        except:
            return 0

    # Maintain checks the current portfolio and sells stocks you currently hold.
    def operate(self, autosave=False):
        try:
            
            # If not yet reached proper update time, simply return.
            interval = timedelta(hours=self.data['chars']['operatinginterval'])
            self.data['nextUpdate'] = self.data['lastUpdate'] + interval
            if self.data['lastUpdate'] is not None and (datetime.now() < self.data['nextUpdate']):
                return

            # Explore and buy new positions
            for _ in range(self.data['chars']['activeness']):
                symb = choice(stock_symbols)
                self.buy(symb, self.buyEvaluate(symb)* 10)
    
            # Maintain current portfolio and sell positions
            current_positions = list(self.data['portfolio'].keys())
            if len(current_positions) > 0:   
                for _ in range(self.data['chars']['activeness']):
                    symb = choice(current_positions)
                    self.sell(symb, self.sellEvaluate(symb)*10)
            
            newEvaluation = self.evaluatePortfolio()

            # If below threshold, kill itself. 
            if newEvaluation < ELIMINATION_THRESHOLD:
                db_bots.delete('id',self.data['id'])
                return


            self.data['evaluations'].append((now(),newEvaluation))
            self.data['value'] = newEvaluation
            self.data['lastUpdate'] = datetime.now()
            if autosave:
                self.save()
        except Exception as e:
            log('Error occurred during operation: {}'.format(e),'error')