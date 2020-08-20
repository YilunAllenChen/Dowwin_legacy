#!/usr/bin/python3
#
# Darwin Robotics, 2020
#

'''
This is the entry point to the Dowwin Core system.
'''
import asyncio
from __log import log, f, LOG_PATH
from _adapter_database import client as sync_client
from _adapter_database_async import client as async_client
from _adapter_database import sync_upload_log
from task_cli import task_CLI
from task_crawler import task_crawler
from task_trainer import task_trainer
from task_arbiter import task_arbiter
from task_scout import task_scout
from task_cache_manager import task_cache_manager

async def Manager():
    '''
    Master task to start all sub tasks
    '''

    loop = asyncio.get_event_loop()
    stop = asyncio.Event()

    tasks = [
        asyncio.ensure_future(task_CLI(loop, stop)),
        asyncio.create_task(task_cache_manager(stop)),
        asyncio.ensure_future(task_crawler(loop, stop)),
        asyncio.ensure_future(task_arbiter(loop, stop)),
        asyncio.ensure_future(task_trainer(loop, stop)),
        asyncio.ensure_future(task_scout(loop, stop)),
    ]

    _returns = await asyncio.gather(*tasks, return_exceptions=False)
    sync_upload_log(LOG_PATH)
    sync_client.close()
    async_client.close()
    f.close()
    sync_upload_log(LOG_PATH)
    
    return
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Manager())

