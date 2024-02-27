import asyncio
from m_worker.worker import Worker


async def main():
    worker = Worker()
    await worker.init_playwright()
    await worker.run()

if __name__ == '__main__':
    asyncio.run(main())
