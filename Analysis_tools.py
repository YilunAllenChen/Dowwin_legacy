from _adapter_database import client
from _adapter_database import sync_get_bots_sorted_by_next_update
from __log import log, vlog
import matplotlib.pyplot as plot

# Test connection to db.

'''
Examples
'''

bots = client['Dowwin']['tradebots']
bots = [item for item in bots.find({}, {'_id': 0, 'nextUpdate': 1})]




bins = [100 * i + 60000 for i in range(700)]
plot.hist([bot.get('nextUpdate') for bot in bots])
plot.show()
