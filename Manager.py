import asyncio
from CLI import CLI
from Courier import Courier
from Trainer import Trainer
from Arbiter import Arbiter

async def Manager():
    loop = asyncio.get_event_loop()
    stop = asyncio.Event()

    tasks = [
        asyncio.ensure_future(CLI(loop, stop), loop=loop),
        asyncio.ensure_future(Courier(loop, stop), loop=loop),
        asyncio.ensure_future(Arbiter(loop, stop), loop=loop),
        asyncio.ensure_future(Trainer(loop, stop), loop=loop)
    ]

    _returns = await asyncio.gather(*tasks, return_exceptions=False)
    return
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Manager())

