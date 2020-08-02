from _database_adapter import db_bots, db_market
from __log import log, vlog
import matplotlib.pyplot as plot

# Test connection to db.
db_bots.test_connection()
log(f'**** Welcome to Dowwin Analysis Toolkit ****\n  - db_bots collection has {db_bots.count()} tradebots.\n  - db_market collection has {db_market.count()} stock data.','ok')




'''
Examples
'''

# A beautified print function.
log("hello.")
# vlog expands a dictionary vertically to better visualize
vlog({'key1': 'value1', 'key2': 'value2'})


# db_bots.get() function gives you a list of tradebots sorted based on nextUpdate timestamp, from earliest to latest
# Parameter 'num' specifices how many tradebots you are getting.
some_bots = db_bots.get(num=200)

# vertically expand the 11th bot
vlog(some_bots[10])

plot.hist([bot.get('value') for bot in some_bots])
plot.show()

# db_market.get("MSFT") function gives you information about the stock abbrevieated as msft (Microsoft Inc.).
msft = db_market.get("MSFT")

# Check the payout ratio of microsoft.
log(msft['payoutRatio'])