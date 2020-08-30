#
# Darwin Robotics, 2020
#

'''
This module contains the core functionalities of Tradebot.
'''


from math import log10
from random import choice, random
from time import time as now
from datetime import datetime, timedelta
from _names import names
from _adapter_database import sync_get_stock, sync_delete_bot, sync_update_bot
from _adapter_database_async import async_get_stock
from _static_data import stock_symbols
from GLOBAL_CONFIG import ELIMINATION_THRESHOLD, STARTING_FUND
from task_cache_manager import market_cache
import asyncio
from __log import log, vlog, debug


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
                'operatinginterval': 6 + 2*int(random()*72) # in hours
            },
            'lastUpdate': datetime.now(),
            'nextUpdate': datetime.now(),
            'created': datetime.now()
        })

    def get(self, symb: str) -> dict:
        '''
        Let the current tradebot obtain the information of a certain stock. It will first look at the local cache. If it's a cache miss
        then go to remote to fetch it.
        
        :param symb: symbol of the stock to get.
        '''
        if symb in market_cache:
            return market_cache[symb]
        else:
            return sync_get_stock(symb)

    def save(self) -> None:
        '''
        Save the tradebot to the remote database.
        '''
        debug(self.stringify_bot(portfolio=False))
        sync_update_bot(self.data,by='id')

    def delete(self):
        '''
        Delete the tradebot from the remote database.
        '''
        log(f'Deleting this bot because its portfolio has fell below the line. {self.stringify_bot()}',to_file=True)
        sync_delete_bot('id',self.data['id'])

    def buy(self, symb: str, shares: float) -> None:
        '''
        Function to buy a certain number of shares of a certain stock. 

        :param symb: Symbol to buy.
        :param shares: How many shares to buy. Floats will be rounded.  
        '''
        shares = int(shares)
        if shares <= 0:
            return
        stock = self.get(symb)
        if stock is None:
            log("Problem obtaining stock [{}]".format(symb),'error')
        if stock['ask'] <= 0.1:
            return

        trans = shares * stock['ask']
        if self.data['cash'] < trans:
            return
        try:
            pick = symb
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
            log("Error occured buying stock {}. Details: {}".format(symb, e))
            raise Exception("Error occured buying stock {}. Details: {}".format(symb, e))
            
        self.data['activities'].append(
            (datetime.now(), shares, symb, stock['ask'], self.data['cash']))

    def sell(self, symb: str, shares: float) -> None:
        '''
        Function to sell a certain number of shares of a certain stock. 

        :param symb: Symbol to sell.
        :param shares: How many shares to sell. Floats will be rounded.  
        '''
        shares = int(shares)
        stock = self.get(symb)
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
            raise Exception("Error occured selling stock {}. Details: {}".format(symb, e))

    def evaluatePortfolio(self) -> float:
        '''
        Get a most up-to-date evaluation of the portfolio.
        '''
        try:
            evalutaion = self.data['cash']
            positions = self.data['portfolio'].items()
            for position in positions:
                price = self.get(position[0]).get('bid')
                if price is None or price < 0.1:
                    price = position[1]['avgcost']
                evalutaion += price * position[1]['shares']
            return round(evalutaion,2)
        except Exception as e:
            raise Exception(f'Unable to evaluate portfolio: {e}')


    def buyEvaluate(self, symb: str) -> float:
        '''
        buyEvaluate computes how many shares of a stock you should buy (If negative then don't buy of course).
        
        :param symb: Symbol of the stock to evaluate
        '''
        stock = self.get(symb)
        try:
            value = 20 * log10(stock.get('marketCap',0)) / stock.get('trailingPE', 0)

            growth = 0.2 * stock.get('fiftyTwoWeekHigh', 0) / stock.get('fiftyTwoWeekLow') * \
                3 * stock.get('beta',1)
            return self.data['chars']['growth'] * growth + self.data['chars']['value'] * value
        except Exception:
            return 0

    def sellEvaluate(self, symb: str) -> float:
        '''
        buyEvaluate computes how many shares of a stock you should buy (If negative then don't buy of course).
        
        :param symb: Symbol of the stock to evaluate
        '''

        stock = self.get(symb)
        try:
            return (stock['bid'] - self.data['portfolio'][symb]['avgcost']) * self.data['chars']['profitmargin']/stock['bid'] * self.data['portfolio'][symb]['shares']
        except:
            return 0

    # Maintain checks the current portfolio and sells stocks you currently hold.
    def operate(self, autosave=False):
        try:
            # If not yet reached proper update time, simply return.
            if self.data['nextUpdate'] is not None and (datetime.now() < self.data['nextUpdate']):
                return

            self.data['lastUpdate'] = datetime.now()
            interval = timedelta(hours=self.data['chars']['operatinginterval'])
            self.data['nextUpdate'] = self.data['lastUpdate'] + timedelta(hours=self.data['chars']['operatinginterval'])

            eyeing_buys = [choice(stock_symbols) for _ in range(self.data['chars']['activeness'])]
            for symb in eyeing_buys:
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
                self.delete()
                return


            self.data['evaluations'].append((now(),newEvaluation))
            self.data['value'] = newEvaluation

            if autosave:
                self.save()
        except Exception as e:
            log('Error occurred during operation: {}'.format(e),'error')


    def stringify_recent_activites(self, item=10) -> str:
        '''
        Get a report on the stock's recent activites

        :param item: number of activities reported
        '''
        data = self.data
        res = '\nRecent Activities: \n\n'
        count = -min([len(data['activities']), item])
        for item in data['activities'][count::]:
            timestamp = str(item[0])
            action = '\033[92mBUYED\033[0m' if item[1] > 0 else '\033[91mSOLD \033[0m'
            stock = item[2]
            shares = abs(item[1])
            price = item[3]
            res += f'[{timestamp}] {action} {shares} of {stock} at price {price}\n'
        return res

    def stringify_portfolio(self) -> str:
        value = self.data['value']
        res = '\nPortfolio: \n\n'
        portfolio = self.data['portfolio']
        for position in portfolio:
            shares = portfolio[position]["shares"]
            avgcost = portfolio[position]["avgcost"]
            position_value = shares * avgcost
            diversity = str(round(position_value / value * 100, 2)) + '%'
            res += f'{position}: {shares} shares at {avgcost}, total value: {position_value}, portfolio diversity: {diversity}\n'
        return res

    def stringify_bot(self, activites=True, portfolio=True) -> str:
        '''
        Get a report of the bot's evaluations and recent activities 
        '''
        data = self.data
        res = f"Tradebot {data['id']} : {data['name']}. \nValue: {data['value']} | Cash: {data['cash']}\n"
        if activites:
            res += self.stringify_recent_activites()
        if portfolio:
            res += self.stringify_portfolio()
        return res