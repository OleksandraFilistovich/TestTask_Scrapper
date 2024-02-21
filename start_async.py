import aiohttp
import asyncio
from app.modules.car import CarInfo

from app.modules.scrapper import DataScrapperAsync

PAGE_START = 1


class Bot:
    def __init__(self):
        self.tasks: list = []
        self.pages_end = False
        self.page_num = PAGE_START
        self.max_tasks = 5
        self.cars: list = []

    def bulk_save(self):
        return len(self.cars)

    async def main(self):
        async with aiohttp.ClientSession() as session:

            while not self.pages_end:
                while len(self.tasks) >= self.max_tasks:
                    await asyncio.sleep(0.1)

                    for task in self.tasks[:]:
                        if task.done():
                            self.tasks.remove(task)

                    self.bulk_save()
                    
                task = asyncio.create_task(self.collecting_info(session, self.page_num))
                self.tasks.append(task)

                self.page_num += 1


    async def collecting_info(self, session, page: int):
        """Goes through found car pages in bunches,
        prints car info if possible,
        then goes to find more on next page."""
        print("= Links search start =")
        print(f"= {page} page search =")

        scrapper = DataScrapperAsync(session)
        links = await scrapper.links(page)

        if not links:
            self.pages_end = True
            print("= Pages ended =")

            return

        for link in links:
            car = await scrapper.page_processing(link)
            self.cars.append(car)

            print(f"In page {page}: {car.url}")

        print(f"= {page} page ended =")
        return True


if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.main())
