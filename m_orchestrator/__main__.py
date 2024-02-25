import asyncio

from m_orchestrator.orchestaror import Orchestrator
from utils.rs import Cache_Tasks

o = Orchestrator()
asyncio.run(o.run())
#o.bulk_save()
#async def load():
#    asyncio.run(check())
