from __log import log
from _database_adapter import db_bots


async def task_CLI(loop, stop, debug=False):
    log("*** Command Line Utilities Online. Click q to quit. *** ",'ok')
    while not stop.is_set():
        command = await loop.run_in_executor(None, input, "")
        if 'q' in command:
            stop.set()
        if 'r' in command:
            report()
    log("*** CLI Handler is shutting down ***",'ok')


def report():
    log("What's up.")
