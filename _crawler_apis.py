#
# Darwin Robotics, 2020
#

'''
This module provides APIs for the crawler to acquire market data.
'''

from requests import get
import pandas as pd
import json
import re
import asyncio
from __log import log


class Ticker():
    def __init__(self, symb: str):
        '''
        Create a Ticker with given symbol. Unless directed, the Ticker won't update its data.
        
        :param symb: The stock symbol.
        '''
        self.symb = symb
        self.ticker_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symb}"
        self.info_url = f"https://finance.yahoo.com/quote/{symb}"

        self.raw = {}
        self.info = {}
        self.reco = {}

    def blocking_get(self, proxy) -> str:
        '''
        Function returns the raw html of the Ticker's associated info_url.
        
        :param proxy: Option to use proxy.
        TODO(Allen Chen): figure out async ways to do this
        '''
        html = get(url=self.info_url, proxies=proxy).text
        return html

    async def update(self, proxy=None) -> dict:
        '''
        function runs the get function and parse it to extract the useful information, then store
        it into self.raw, self.info and self.reco.

        :param proxy: Option to use proxy for the get.
        '''
        # Retry if not reached
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, self.blocking_get, proxy)

        json_str = html.split('root.App.main =')[1].split(
            '(this)')[0].split(';\n}')[0].strip()
        data = json.loads(json_str)[
            'context']['dispatcher']['stores']['QuoteSummaryStore']
        # return data
        data = json.dumps(data).replace('{}', 'null')
        data = re.sub(
            r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', data)
        data = json.loads(data)

        self.raw = data
        self.info = data.get('summaryDetail')
        self.reco = data.get('upgradeDowngradeHistory')
