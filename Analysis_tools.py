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
bots = [item for item in bots.find({}, {'_id':0, 'id': 1, 'nextUpdate': 1, 'value': 1})]


fig, axs = plot.subplots(2,2)
fig.suptitle('Dowwin Analysis Toolkit Dashboard')

bins_value = [100 * i + 60000 for i in range(700)]
bins_nextUpdate = [timedelta(hours=1) * i + datetime.now() for i in range (144)]

axs[0][0].hist([bot.get('value') for bot in bots], bins=bins_value)

axs[0][1].hist([bot.get('nextUpdate') for bot in bots], bins=bins_nextUpdate)
plot.show()