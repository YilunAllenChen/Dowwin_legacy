from log import *


async def CLI(loop, stop):
    log("Press 'q' to shutdown the HVT Request Bot and quit the application: ")
    while not stop.is_set():
        command = await loop.run_in_executor(None, input, "")
        if 'q' in command:
            stop.set()
    log("***** CLI Handler is shutting down *****",'ok')


