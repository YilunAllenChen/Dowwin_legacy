from names import names
from random import choice, random
from time import time as now
from database_adapter import Market_Adapter
from math import log10
from static_data import SP500


class Tradebot():
    def __init__(self, **kwargs):
        self.market = Market_Adapter()
        self.data = kwargs.get("data", {
            'id': now()*1000,
            'name': choice(names),
            'cash': 100000,
            'portfolio': {},
            'activities': [],
            'evaluations': [],
            'chars': {
                'growth': random(),
                'value': random(),
                'profitmargin': random(),
                'stoplossmargin': random(),
                'activeness': int(random()*100)
            },
            'lastUpdate': now() * 1000
        })

    def selfcheck(self):
        return

    def buy(self, symb, shares):
        shares = int(shares)
        if shares <= 0:
            #print("Cannot buy less than or equal to 0 share")
            return
        stock = self.market.get(symb)
        if stock is None:
            raise Exception("Can't obtain target stock")
        if stock['ask'] <= 0.1:
            raise Exception("Stock ask is below 0.1.")
        trans = shares * stock['ask']
        if self.data['cash'] < trans:
            #print("Insufficient Cash")
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
            (now()*1000, shares, symb, stock['ask'], self.data['cash']))

    # sell 'shares' number of a certain stock. Stock is of dict type containing information 'symbol', 'ask' and 'bid'.
    def sell(self, symb, shares):
        stock = self.market.get(symb)
        pick = symb
        if pick not in self.data['portfolio']:
            raise Exception("Can't sell stock that you don't have")
        sellshares = min([self.data['portfolio'][pick]['shares'], int(shares)])
        if sellshares <= 0:
            #print("Can't sell any more shares of", symb)
            return
        if stock['bid'] <= 0.1:
            raise Exception("Something's wrong with market data")

        try:
            self.data['cash'] += stock['bid'] * shares
            if self.data['portfolio'][pick]['shares'] == sellshares:
                self.data['portfolio'].pop(pick)
            else:
                self.data['portfolio'][pick]['shares'] -= shares
            self.data['activities'].append(
                (now()*1000, -shares, symb, stock['bid'], self.data['cash']))
        except Exception as e:
            raise e

    def evaluatePortfolio(self):
        evalutaion = self.data['cash']
        positions = self.data['portfolio'].items()
        for position in positions:
            price = self.market.get(position[0])['bid']
            if price < 0.1:
                raise Exception("Invalid Price")
            evalutaion += price * position[1]['shares']
        return evalutaion

    # buyEvaluate computes how many shares of a stock should you buy (If negative then don't buy of course).
    # TODO: Develop a better evaluation algorithm.
    def buyEvaluate(self, symb):
        stock = self.market.get(symb)
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
        stock = self.market.get(symb)
        try:
            return (stock['bid'] - self.data['portfolio'][symb]['avgcost']) * self.data['chars']['profitmargin']/stock['bid'] * self.portfolio[symb]['shares']
        except:
            return 0

    # Maintain checks the current portfolio and sells stocks you currently hold.
    def operate(self):
        
        # Explore and buy new positions
        for i in range(self.data['chars']['activeness']):
            symb = choice(SP500)
            self.buy(symb, self.buyEvaluate(symb)* 10)

 
        # Maintain current portfolio and sell positions
        for i in range(self.data['chars']['activeness']):
            symb = choice(list(self.data['portfolio'].keys()))
            self.sell(symb, self.sellEvaluate(symb)*10)
        
        newEvaluation = self.evaluatePortfolio()
        self.data['evaluations'].append((now(),newEvaluation))
        self.data['lastUpdate'] = now()
        return self.data