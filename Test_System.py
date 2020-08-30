import sys
sys.path.extend(['tasks', 'adapters_apis', 'static_data', 'utility_modules'])


import unittest
from __log import log
import adapters_apis._adapter_database as api_db
from utility_modules._Trader import Tradebot
import utility_modules._Trader
from tasks.task_cache_manager import market_cache
import tasks.task_cache_manager
from pprint import pformat as pf


class DowwinTestingFramework(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.db = api_db.client['Dowwin']['System_test']
        
    def test_db_connection(self):
        self.db = api_db.client['Dowwin']['System_test']
        self.db.insert_one({'test':'done'})
        self.db.delete_many({})
        log("Database connection established", 'ok')

    def test_db_create_bot(self):
        newbot = Tradebot()
        log(f"New bot Initialized with chars:\n{pf(newbot.data['chars'])}",'ok')
    
        


if __name__ == '__main__':
    unittest.main()