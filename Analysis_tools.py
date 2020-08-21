from _adapter_database import client
from _adapter_database import sync_get_bots_sorted_by_next_update
from __log import log, vlog
import matplotlib.pyplot as plot
from datetime import datetime, timedelta

# Test connection to db.

'''
Examples
'''

bots = client['Dowwin']['tradebots']
bots = [item for item in bots.find({}, {'_id': 0, 'nextUpdate': 1})]




bins = [100 * i + 60000 for i in range(700)]
bins = [timedelta(hours=1) * i + datetime.now() for i in range (144)]
plot.hist([bot.get('nextUpdate') for bot in bots], bins=bins)
plot.show()
