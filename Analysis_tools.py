from _adapter_database import client
from _adapter_database import sync_get_bots_sorted_by_next_update, sync_delete_bot
from __log import log, vlog
import matplotlib.pyplot as plot
from datetime import datetime, timedelta

# Test connection to db.

'''
Examples
'''

bots = client['Dowwin']['tradebots']
bots = [item for item in bots.find({}, {'_id':0, 'id': 1, 'chars': 1})]




bins = [100 * i + 60000 for i in range(700)]
bins = [timedelta(hours=1) * i + datetime.now() for i in range (144)]
bins = [i for i in range(200)]
plot.hist([bot.get('chars').get('operatinginterval') for bot in bots], bins=bins)
plot.show()

