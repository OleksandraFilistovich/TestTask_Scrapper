from playwright.sync_api import sync_playwright

from app.modules.scrapper_parsel import DataScrapperParsel

PAGE_START = 11


class Bot:
    def __init__(self):
        self.page_num = PAGE_START
        self.pages_end = False
        self.cars: list = {}

    def bulk_save(self):
        pass 
    
    def run(self, scrapper: DataScrapperParsel):

        while not self.pages_end:

            print(f"= {self.page_num} page search =")
            links = scrapper.collect_links(self.page_num)

            if not links:
                self.pages_end = True
                print("= Pages ended =")
                return
            for link in links:
                car = scrapper.collecting_data(link)
                print(f"Found car: {car.url}")

            print(f"= {self.page_num} page ended =")
            self.page_num += 1


if __name__ == "__main__":
    bot = Bot()

    with sync_playwright() as p:

        browser = p.chromium.launch()
        browser_page = browser.new_page()

        scrapper = DataScrapperParsel(browser_page)
        bot.run(scrapper)

    browser.close()
