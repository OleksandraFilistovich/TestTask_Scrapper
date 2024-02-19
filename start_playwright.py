from playwright.sync_api import sync_playwright

from app.modules.scrapper import DataScrapperPW

PAGE_START = 1


class Bot:
    def __init__(self):
        self.page_num = PAGE_START
        self.pages_end = False
        self.cars: list = {}

    def bulk_save(self):
        pass

    def collecting_info(self, page_num: int, page):
        """Goes through found car pages in bunches,
        stores car info."""
        print("= Links search start =")
        print(f"= {page_num} page search =")

        scrapper = DataScrapperPW(page)
        links = scrapper.links(page_num)

        if not links:
            self.pages_end = True
            print("= Pages ended =")
            return
        for link in links:
            car = scrapper.page_processing(link)
            self.cars[car.url] = car
            print(f"Found car: {car.url} \n number: {car.phone_number}")

        print(f"= {page_num} page ended =")
        return True

    def run(self):
        with sync_playwright() as p:

            browser = p.chromium.launch()
            page_obj = browser.new_page()

            while not self.pages_end:
            
                result = self.collecting_info(self.page_num, page_obj)
                self.page_num += 1
                
                self.bulk_save()

            browser.close()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
