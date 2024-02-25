from playwright.async_api import Page

from utils.car import CarInfo
from utils.rs import Cache_Tasks
from utils.scrapper_parsel import DataScrapperParselAsync


class Worker:
    def __init__(self, page: int):
        self.page_num = page
        self.cars: list = []

    
    async def collecting_info(self,
                              page: Page,
                              cache: Cache_Tasks) -> list[CarInfo]:
        cache.update_task(self.page_num)
        scrapper = DataScrapperParselAsync(page)

        print(f"= {self.page_num} page search =")
        links = await scrapper.collect_links(self.page_num)

        if not links:
            print("= Pages ended =")
            await page.close()
            return None
        
        for link in links:
            car = await scrapper.collecting_data(link)
            print(f"Found car on {self.page_num}: {car.url}")
            self.cars.append(car.to_dict())

        print(f"= {self.page_num} page ended =")
        cache.add_results(self.page_num, self.cars)
        await page.close()
        
