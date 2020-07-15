import asyncio
from __log import log
from _database_adapter import client
from task_cli import task_CLI
from task_crawler import task_crawler
from task_trainer import task_trainer
from task_arbiter import task_arbiter

async def Manager():
    
    loop = asyncio.get_event_loop()
    stop = asyncio.Event()

    tasks = [
        asyncio.ensure_future(task_CLI(loop, stop, debug=False)),
        asyncio.ensure_future(task_crawler(loop, stop, debug=False)),
        asyncio.ensure_future(task_arbiter(loop, stop, debug=False)),
        asyncio.ensure_future(task_trainer(loop, stop, debug=False))
    ]

    _returns = await asyncio.gather(*tasks, return_exceptions=False)
    client.close()
    return
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Manager())

