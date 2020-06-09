'''
This module provides numerous common APIs to access data in the database.
'''


from config import db_market
from json import load

# Parameter way can be 'fs' or 'db' at this moment, pointing to JSON-formatted local data(slow) or mongoDB(fast).
def getInfo(symb, way='fs'):
    try:
        if way == 'db':
            data = db_market.find_one({'Symb': symb})
            return data['Info'] if data is not None else None
        elif way == 'fs':
            data = open('dataset_static/' +
                        symb + '.json', 'r')
            stock = load(data)['Info']
            data.close()
            return stock
    except Exception as e:
        print("Error getting info. ",e)
        raise

