# Infrastructure
from random import random, choice
import threading
import sys
from time import sleep, time
from math import log10
from json import load


# yfinance library provides APIs to access live stock market data
import yfinance as yf

# customized data libraries
from SymbList import SP500
from names import names

# apis give useful APIs to obtain data.
from apis import getInfo

# config gives acess to market and bots.
from config import db_market, db_bots, forestSize

# Macro functions
def createTimeStamp(): return int(round(time() * 1000))
def createName(): return choice(names)
# getInfo macro returns the stock data used in buy, sell and evaluate.


class Bot:

    # Init function: If given epoch data then use that data. Else generate randomly.
    def __init__(self, epoch={
        'cash': 100000,
        'portfolio': {},
    }):
        try:
            self.name = epoch['name'] if 'name' in epoch else createName()
            self.id = epoch['id'] if 'id' in epoch else createTimeStamp()
            self.cash = epoch['cash']
            self.portfolio = epoch['portfolio']
            self.chars = epoch['chars'] if 'chars' in epoch else {
                'growth': random(),
                'value': random(),
                'profitmargin': random()/5,
                'stoplossmargin': random()/5,
            }
            self.db_bots = db_bots
            self.history = epoch['history'] if 'history' in epoch else {
                'evaluation': [],
                'operations': []
            }
        except Exception as e:
            print("Failed to initialize metadata: ", e)
            raise

    # Perform a self check on data validity.
    # TODO: perform more checks other than cash.
    def selfcheck(self):
        if self.cash < 0:
            raise Exception("Self-check::CashIsNegative")

    # Save the current bot to mongoDB.
    def save(self):
        try:
            doc = {
                'id': self.id,
                'cash': self.cash,
                'portfolio': self.portfolio,
                'chars': self.chars,
                'name': self.name,
                'history': self.history
            }
            self.db_bots.replace_one({'id': doc['id']}, doc, True)
        except Exception as e:
            print("Failed to save: ", e)
            raise
    # delete the current bot to mongoDB.

    def delete(self):
        try:
            self.db_bots.delete_one({'id': self.id})
        except Exception as e:
            print("Failed to delete: ", e)
            raise

    # buy 'shares' number of a certain stock. Stock is of dict type containing information 'symbol', 'ask' and 'bid'.
    # TODO: for each position in the portfolio, add additional useful information other than avgCost. For example, buy/sell history.

    def buy(self, stock: dict, shares):
        shares = int(shares)
        if shares <= 0 or stock['ask'] <= 0.1:
            return
        trans = shares * stock['ask']
        if self.cash < trans:
            return

        else:
            try:
                pick = stock['symbol']
                if pick in self.portfolio:
                    position = self.portfolio[pick]
                    newAvgCost = (
                        position['avgcost'] * position['shares'] + trans) / (shares + position['shares'])
                    position['avgcost'] = newAvgCost
                    position['shares'] += shares
                else:
                    self.portfolio[stock['symbol']] = {
                        'shares': shares, 'avgcost': stock['ask']}
                self.cash -= trans
            except Exception as e:
                print("Error buying, ", e)
                raise
        self.history['operations'].append(
            (createTimeStamp(), shares, stock['symbol'], stock['bid'], self.cash))

    # sell 'shares' number of a certain stock. Stock is of dict type containing information 'symbol', 'ask' and 'bid'.
    def sell(self, stock: dict, shares):
        pick = stock['symbol']
        if pick not in self.portfolio:
            return
        sellshares = min([self.portfolio[pick]['shares'], int(shares)])
        if sellshares <= 0 or stock['bid'] <= 0.1:
            return

        try:
            self.cash += stock['bid'] * shares
            if self.portfolio[pick]['shares'] == sellshares:
                self.portfolio.pop(pick)
            else:
                self.portfolio[pick]['shares'] -= shares
            self.history['operations'].append(
                (createTimeStamp(), -shares, stock['symbol'], stock['bid'], self.cash))
        except Exception as e:
            print("Error selling, ", e)
            raise

    # Function to evaluate all current positions by 'bid' price.
    # TODO: Give an analysis (maybe graphical?) on the portfolio.
    def evaluatePortfolio(self, way):
        value = self.cash
        for key in self.portfolio:
            item = self.portfolio[key]
            stock = getInfo(key, way=way)
            value += stock['bid'] * item['shares']
        return value

    # buyEvaluate computes how many shares of a stock should you buy (If negative then don't buy of course).
    # TODO: Develop a better evaluation algorithm.
    def buyEvaluate(self, stock: dict):
        try:
            value = log10(stock['marketCap']) / stock['trailingPE']
            growth = 10 * stock['52WeekChange'] * \
                stock['beta'] + 10 * stock['earningsQuarterlyGrowth']
            return self.chars['growth'] * growth + self.chars['value'] * value
        except:
            return 0

    # sellEvaluate computes how many shares of a stock should you sell (If negative then don't sell of course).
    # TODO: Develop a better evaluation algorithm.
    def sellEvaluate(self, stock: dict):
        try:
            return (stock['bid'] - self.portfolio[stock['symbol']]['avgcost']) * self.chars['profitmargin']/stock['bid'] * self.portfolio[stock['symbol']]['shares']
        except:
            return 0

    # Maintain checks the current portfolio and sells stocks you currently hold.
    def maintain(self, way):
        if len(self.portfolio.keys()) == 0:
            return
        for i in range(100):
            stock = getInfo(choice(list(self.portfolio.keys())), way=way)
            self.sell(stock, self.sellEvaluate(
                stock)*10)

    # Explore goes out and evaluate random stocks to buy.
    def explore(self, way):
        for i in range(100):
            stock = getInfo(choice(SP500), way=way)
            self.buy(stock, self.buyEvaluate(stock)
                     * 10)

    # Sell all current positions.
    def sellAll(self, way):
        while(len(self.portfolio) != 0):
            key = choice(list(self.portfolio.keys()))
            stock = getInfo(key, way=way)
            self.sell(stock, self.portfolio[key]['shares'])
        print("Ended up with value: ", self.cash)

    # A macro combination of explore and maintain.
    # TODO: give more details.
    def operate(self, way='fs'):
        self.explore(way=way)
        self.maintain(way=way)
        value = self.evaluatePortfolio(way=way)
        self.history['evaluation'].append((createTimeStamp(), value))

        recents, recents_str = self.history['operations'][-5:], ''
        for each in recents:
            if each[1] < 0:
                recents_str += '\n' + "\033[91m Selled \033[00m" + str(-int(each[1])) + ' shares of ' + each[2]
            else:
                recents_str += '\n' + "\033[92m Buyed  \033[00m" + str(int(each[1])) + ' shares of ' + each[2]
        recents_str += '\r'

        if value < 80000:
            print("Bot", self.id, self.name,
                  "ended up losing 20 percent value on its trading strategy and is therefore eliminiated.")
            self.delete()
        else:
            for i in range(len(recents)+2):
                sys.stdout.write("\x1b[1A\x1b[2K")
            print("Tradebot {0} {1}{2} has survived another day with evaluation: {3}".format(
                self.id%100000, self.name, (30-len(self.name))*' ', int(value)
            ))
            print(recents_str)

            self.save()

    def eliminate(self, way='fs', bar=100000):
        value = self.evaluatePortfolio(way=way)
        
        if value < bar:
            print("Bot", self.id, self.name,
                  "ended up losing too much value on its trading strategy and is therefore eliminiated.")
            self.delete()
        else:
            print("Tradebot {0} {1}{2} has survived another day with evaluation: {3}".format(
                self.id%100000, self.name, (30-len(self.name))*' ', int(value)
            ))
            sys.stdout.write("\x1b[1A\x1b[2K")
