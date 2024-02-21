import asyncio
from playwright.async_api import async_playwright, Playwright

from app.modules.scrapper_parsel import DataScrapperParselAsync
from app.modules.scrapper import DataScrapperAsync

PAGE_START = 1


class Bot:
    def __init__(self):
        self.tasks: list = []
        self.max_tasks = 3
        self.page_num = PAGE_START
        self.pages_end = False
        self.cars: list = []

    def bulk_save(self):
        return len(self.cars)
    
    async def collecting_info(self, page_num: int, scrapper: DataScrapperParselAsync):

        print(f"= {page_num} page search =")
        links = await scrapper.collect_links(page_num)

        if not links:
            self.pages_end = True
            print("= Pages ended =")

            return
        
        for link in links:
            print(link)
            car = await scrapper.collecting_data(link)
            print(f"Found car: {car.url}")
            self.cars.append(car)

        print(f"= {page_num} page ended =")
        return True


    async def main(self):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch()

            browser_page = await browser.new_page()
            #scrapper = DataScrapperParselAsync(browser_page)
            scrapper = DataScrapperAsync(browser_page)

            while not self.pages_end:
                
                while len(self.tasks) >= self.max_tasks:

                    await asyncio.sleep(0.1)

                    for task in self.tasks[:]:
                        if task.done():
                            self.tasks.remove(task)
                    
                    print(self.bulk_save())

                print("==New==")
                task = asyncio.create_task(self.collecting_info(self.page_num, scrapper))
                self.tasks.append(task)
                

                self.page_num += 1

        await browser.close()


if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.main())