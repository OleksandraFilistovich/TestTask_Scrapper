import asyncio
import aioredis

from envs import REDIS_PASSWORD, REDIS_PORT, REDIS_HOST


class Cache:
    def __init__(self, number_db: int, host: str = REDIS_HOST, port: int = REDIS_PORT, password: str = REDIS_PASSWORD):
        self.red = aioredis.Redis(host=host, port=port, db=number_db, password=password, decode_responses=True)
        self.pipeline = self.red.pipeline()

    async def get(self, name: str):
        while True:
            await asyncio.sleep(0.1)
            try:
                return await self.red.get(name)
            except:
                pass


async def main():
    cache_2 = Cache(2)
    await cache_2.red.incrby('foo', 1)
    print(await cache_2.get('foo'))


if __name__ == '__main__':
    asyncio.run(main())