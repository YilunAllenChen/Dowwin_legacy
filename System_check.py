#
# Darwin Robotics, 2020
#

'''
This module defines a trainer task to train tradebots.
'''

from _Trader import Tradebot
from _adapter_database import sync_get_bots_sorted_by_next_update
from __log import log
from time import sleep
import asyncio
