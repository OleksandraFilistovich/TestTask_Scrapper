import asyncio
from m_orchestrator.orchestaror import Orchestrator


async def main():
    orchestrator = Orchestrator()
    await orchestrator.run()

if __name__ == '__main__':
    asyncio.run(main())
