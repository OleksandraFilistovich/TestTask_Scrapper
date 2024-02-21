import asyncio
from playwright.async_api import async_playwright, Playwright, Page

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
    
    async def collecting_info(self, page_num: int, page: Page):
        scrapper = DataScrapperParselAsync(page)

        print(f"= {page_num} page search =")
        links = await scrapper.collect_links(page_num)

        if not links:
            self.pages_end = True
            print("= Pages ended =")
            await page.close()
            return
        
        for link in links:
            car = await scrapper.collecting_data(link)
            print(f"Found car on {page_num}: {car.url}")
            self.cars.append(car)

        print(f"= {page_num} page ended =")
        await page.close()
        return True

    def clear_tasks(self):
        for task in self.tasks[:]:
            if task.done():
                self.tasks.remove(task)

    async def main(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context()

            while not self.pages_end:
                page = await context.new_page()

                while len(self.tasks) >= self.max_tasks:
                    self.clear_tasks()
                    await asyncio.sleep(0.01)
                else:
                    print(self.bulk_save())

                print("==New==")
                task = asyncio.create_task(self.collecting_info(self.page_num, page))
                self.tasks.append(task)
                
                self.page_num += 1

        await browser.close()


if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.main())
