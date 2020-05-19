from config import market
from json import load

# Parameter way can be 'fs' or 'db' at this moment, pointing to JSON-formatted local data(slow) or mongoDB(fast).
def getInfo(symb, way='fs'):
    if way == 'db':
        return market.find_one({'Symb': symb})
    elif way == 'fs':
        data = open('dataset_static/' +
                    symb + '.json', 'r')
        stock = load(data)['Info']
        data.close()
        return stock
