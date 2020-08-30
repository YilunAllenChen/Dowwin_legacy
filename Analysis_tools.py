
import sys
sys.path.extend(['tasks', 'adapters_apis', 'static_data', 'utility_modules'])



from task_cache_manager import market_cache
from _adapter_database import sync_get_market_image_minimal
from __log import log
from pprint import pformat
from datetime import datetime, timedelta


log("Fetching market data...")
all_stock_data = sync_get_market_image_minimal()
log("Data fetched. Processing...")
market = {}
for item in all_stock_data:
    market[item.get('Symb')] = item.get('Info')

with open("market_data.py",'w') as f:
    f.writelines(pformat(market))
