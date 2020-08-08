#
# Darwin Robotics, 2020
#

'''
This module provides command line utilities for the system.
'''

from __log import log
from _adapter_database import db_bots
from task_cache_manager import market_cache


async def task_CLI(loop, stop):
    log("*** Command Line Utilities Online. Click q to quit. *** ",'ok')
    while not stop.is_set():
        command = await loop.run_in_executor(None, input, "")
        if 'q' in command:
            stop.set()
        if 'r' in command:
            report()
    log("*** CLI Handler is shutting down ***",'ok')


def report():
    log(market_cache)

