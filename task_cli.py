from __log import log


async def task_CLI(loop, stop):
    log("***** Command Line Utilities Online. Click q to quit. ***** ")
    while not stop.is_set():
        command = await loop.run_in_executor(None, input, "")
        if 'q' in command:
            stop.set()
    log("***** CLI Handler is shutting down *****",'ok')


