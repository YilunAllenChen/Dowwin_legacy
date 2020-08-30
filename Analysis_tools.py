from _database_adapter import db_bots, db_market
from __log import log


# A customized logging function, expands dictionary vertically. Feel free to add more customized functions yourselves.
def vlog(data: dict):
    content = '\n'
    for key in data.keys():
        content += f'{key} : {data[key]}\n'
    log(content)

# Test connection to db.
db_bots.test_connection()
log(f'**** Welcome to Dowwin Analysis Toolkit ****\n  - db_bots collection has {db_bots.count()} tradebots.\n  - db_market collection has {db_market.count()} stock data.','ok')




'''
Examples


# A beautified print function.
log("hello.")
# vlog expands a dictionary vertically to better visualize
vlog({'key1': 'value1', 'key2': 'value2'})


# db_bots.get() function gives you a list of tradebots sorted based on nextUpdate timestamp, from earliest to latest
# Parameter 'num' specifices how many tradebots you are getting.
'''
some_bots = db_bots.get(num=20)

# vertically expand the 11th bot

vlog(some_bots[19])


#log(some_bots[99]["cash"])
#log(len(some_bots[19]["activities"]))

lsCash=[]
lsGrowth = []
lsValue = []
lsProfMarg = []
lsStopMarg = []
lsAct = []
lsOptInt =[] 
for i in range(999):
    lsCash.append(some_bots[i]["value"])
    lsGrowth.append(some_bots[i]["chars"]['growth'])
    lsValue.append(some_bots[i]["chars"]['value'])
    lsProfMarg.append(some_bots[i]["chars"]['profitmargin'])
    lsStopMarg.append(some_bots[i]["chars"]['stoplossmargin'])
    lsAct.append(some_bots[i]["chars"]['activeness'])
    lsOptInt.append(some_bots[i]["chars"]['operatinginterval'])
print("The Cash list is :",lsCash)
print("The Growth list is :",lsGrowth)
print("The Value list is :",lsValue)
print("The ProfMarg list is :",lsProfMarg)
print("The StopMarg list is :",lsStopMarg)
print("The Act list is :",lsAct)
print("The OptInt list is :",lsOptInt)

    



'''
# db_market.get("MSFT") function gives you information about the stock abbrevieated as msft (Microsoft Inc.).
msft = db_market.get("MSFT") 

# Check the payout ratio of microsoft.
log(msft['payoutRatio'])
vlog(msft)
'''