from database_adapter import Market_Adapter, Bots_Adapter
from trainer import Trainer
from time import sleep
from datetime import datetime as dt


class TrainingManager():

    def __init__(self):
        self.db_bots = Bots_Adapter()
        self.log = open('trainer_logs/{}.txt'.format(str(dt.now())),'w+')
        self.market_cache = {}

    def get_bot_batch(self):
        self.trainees = self.db_bots.get(num=100)

    def create_bots(self,num=1000):
        for i in range(num):
            bot = Trainer()
            self.save(bot)

    def save(self,bot):
        self.db_bots.update(bot.data,by='id')

    def train(self): 
        count = 0
        for trainee in self.trainees:
            bot = Trainer(data=trainee)
            bot.operate()
            self.save(bot)
            count += 1
        self.log.write("[{}] Training finished with current batch. Total trained: {}".format(str(dt.now()),count))
        self.trainees = []
        return count




trainer = TrainingManager()
while True:
    try:
        trainer.get_bot_batch()
        trainer.train()
    except Exception as e:
        trainer.log.write('[{}] Exception encountered: {}'.format(str(dt.now()),e))
        trainer.log.close()
        exit()