from _adapter_database import client
from _adapter_database import db_bots
from __log import log, vlog
import matplotlib.pyplot as plot

# Test connection to db.
db_bots.test_connection()
log(
    f'**** Welcome to Dowwin Analysis Toolkit ****\n  - db_bots collection has {db_bots.count()} tradebots.\n','ok')


'''
Examples
'''

# A beautified print function.
# log("hello.")
# vlog expands a dictionary vertically to better visualize
# vlog({'key1': 'value1', 'key2': 'value2'})


# db_bots.get() function gives you a list of tradebots sorted based on nextUpdate timestamp, from earliest to latest
# Parameter 'num' specifices how many tradebots you are getting.
# some_bots = db_bots.get(num=200)

# vertically expand the 11th bot
# vlog(some_bots[10])

# plot.hist([bot.get('value') for bot in some_bots])
# plot.show()

# db_market.get("MSFT") function gives you information about the stock abbrevieated as msft (Microsoft Inc.).
# msft = db_market.get("MSFT")

# Check the payout ratio of microsoft.
# log(msft['payoutRatio'])


bots = client['Dowwin']['tradebots']
bots = [item for item in bots.find({}, {'_id': 0, 'value': 1})]

bins = [1000 * i + 60000 for i in range(60)]
plot.hist([bot.get('value') for bot in bots], bins=bins)
plot.show()
