import yfinance as yf
from database_adapter import Market_Adapter
from static_data import SP500
from time import sleep


market = Market_Adapter()


while(True):
    for symb in SP500:
        try:
            ticker = yf.Ticker(symb)
            data = {
                'Symb': symb,
                'Info': ticker.get_info()
            }
            market.update(data,by='Symb')
            print('Data acquired for',symb)
        except Exception as e:
            print(e)
        sleep(3)