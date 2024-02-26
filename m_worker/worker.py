import asyncio
from playwright.async_api import async_playwright, Page, BrowserContext

from utils.car import CarInfo
from utils.rs import Cache_Tasks
from utils.scrapper_parsel import DataScrapperParselAsync


CACHE = Cache_Tasks()

class Worker:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.tasks_list = []
        self.max_tasks = 3
        self.cars: list = []

    async def init_playwright(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)

    def clear_tasks(self):
        for task in self.tasks_list[:]:
            if task.done():
                self.tasks_list.remove(task)

    async def collecting_info(self, page: Page, page_num: int) -> list[CarInfo]:
        scrapper = DataScrapperParselAsync(page)

        print(f"= {page_num} page search =")
        links = await scrapper.collect_links(page_num)

        if not links:
            print("= Pages ended =")
            await page.close()
            return None
        
        for link in links:
            car = await scrapper.collecting_data(link)
            print(f"Found car on {page_num}: {car.url}")
            self.cars.append(car.to_dict())

        print(f"= {page_num} page ended =")
        CACHE.add_results(page_num, self.cars)
        await page.close()
        
    async def run_worker(self, context : BrowserContext, page_num: int):
        while len(self.tasks_list) >= self.max_tasks:
            self.clear_tasks()
            await asyncio.sleep(0.01)

        print(f'worker took {page_num}')

        browser_page = await context.new_page()

        task = asyncio.create_task(self.collecting_info(browser_page, page_num))
        self.tasks_list.append(task)
    
    async def run(self):
        context = await self.browser.new_context()

        while True:
            #  *Takes not done tasks from redis
            tasks_to_do = CACHE.get_tasks()
            
            if len(tasks_to_do) >= 2:
                print(tasks_to_do)

                for task in tasks_to_do:
                    await self.run_worker(context, task)
                    
                while len(self.tasks_list) > 0:
                    self.clear_tasks()
                    await asyncio.sleep(0.01)
                break
            else:
                continue
            
        await self.browser.close()
        await self.playwright.stop()
        
        print("WORKER STOPPED")