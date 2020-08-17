from _adapter_database import client
from _adapter_database import sync_get_bots_sorted_by_next_update
from __log import log, vlog
import matplotlib.pyplot as plot

# Test connection to db.
db_bots.test_connection()
log(
    f'**** Welcome to Dowwin Analysis Toolkit ****\n  - db_bots collection has {db_bots.count()} tradebots.\n','ok')


'''
Examples
'''
sync_get_bots_sorted_by_next_update(num=1000)

bots = client['Dowwin']['tradebots']
bots = [item for item in bots.find({}, {'_id': 0, 'value': 1})]

bins = [1000 * i + 60000 for i in range(60)]
plot.hist([bot.get('value') for bot in bots], bins=bins)
plot.show()
