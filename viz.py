from json import load
import matplotlib as mp
import matplotlib.pyplot as plt

from apis import getInfo


# TODO: Fix this.

def viz(symb):
    data = getInfo(symb,way='db')
    
    ts = data.keys()
    opens = [item['Open'] for item in data['Hist'].values()]
    high = [item['High'] for item in data['Hist'].values()]
    low = [item['Low'] for item in data['Hist'].values()]
    close = [item['Close'] for item in data['Hist'].values()]
    vol = [item['Volume'] for item in data['Hist'].values()]
    dvnd = [item['Open'] for item in data['Hist'].values()]


    allDays = []
    for day in data['Hist'].values():
        allDays.append([day['Open'],day['Close'],day['High'],day['Low']])

    plt.boxplot(allDays)
    plt.show()

viz('MSFT')