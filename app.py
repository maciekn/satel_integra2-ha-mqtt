
import asyncio
from satel_integra2.satel_integra import AsyncSatel
import logging
import os


def outputChanged(status):
    print(status)

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
stl = AsyncSatel(os.environ["ETHM_HOST"],
                    os.environ["ETHM_PORT"],
                    loop,
                    [1, 2],
                    [41]
                    )


loop.run_until_complete(stl.connect())
loop.create_task(stl.keep_alive())
loop.create_task(stl.monitor_status(output_changed_callback=outputChanged, monitoring_query=b'\x7F\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

loop.run_forever()
loop.close()
