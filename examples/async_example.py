import asyncio
import aiohttp


async def get_response(session):
    
    url = 'https://auto.ria.com/uk/auto_vaz_lada_2101_34094199.html'
    async with session.get(url=url) as response:
        response_text = await response.text()

        return response_text


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        task = asyncio.create_task(get_response(session))
        tasks.append(task)


        while tasks:
            await asyncio.sleep(0.001)
            for task in tasks[:]:
                if task.done():
                    result = task.result()
                    print('End:', len(result))
                    tasks.remove(task)


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())
    # loop.run_forever()

    asyncio.run(main())
