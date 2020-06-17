from database_adapter import Market_Adapter, Bots_Adapter
from tradebot import Tradebot
from time import sleep


class Trainer():

    def __init__(self):
        self.db_bots = Bots_Adapter()

        self.market_cache = {}
        self.trainees = self.db_bots.get(num=100)

    def get_bot_batch(self):
        self.trainees = self.db_bots.get(num=100)

    def create_bots(self,num=1000):
        for i in range(num):
            bot = Tradebot()
            self.save(bot)

    def save(self,bot):
        self.db_bots.update(bot.data,by='id')

    def train(self): 
        count = 0
        for trainee in self.trainees:
            bot = Tradebot(data=trainee)
            bot.operate()
            print(bot.data['evaluations'])
            self.save(bot)
            count += 1
        print("Training finished with current batch. Total trained: ", count)
        self.trainees = []
        return count

trainer = Trainer()