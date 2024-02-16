import time
import threading

from app.modules.scrapper import DataScrapper

PAGE_START = 1


class Bot:
    def __init__(self):
        self.threads_list: list[threading.Thread] = []
        self.max_threads = 5
        self.flags_for_stop = {}
        self.page = PAGE_START
        self.pages_end = False
        self.PAGES_END_FLAG = False
        self.cars: list = {}

    def clear_threads(self):
        for thread in self.threads_list[:]:
            if not thread.is_alive():
                self.threads_list.remove(thread)

    def bulk_save(self):
        pass

    def run(self):
        while not self.PAGES_END_FLAG:
            
            self.clear_threads()
            
            while True:
                if len(self.threads_list) < self.max_threads:
                    break
                self.clear_threads()
                time.sleep(0.1)

            x = threading.Thread(target=self.collecting_info, name=f'Thread {self.page}', daemon=True, args=(self.page,))
            x.start()

            print(f"=== {x.name} ===")
            self.page += 1

            self.threads_list.append(x)

            self.bulk_save()

        for thread in self.threads_list:
            thread.join()

    def collecting_info(self, page: int):
        """Goes through found car pages in bunches,
        prints car info if possible,
        then goes to find more on next page."""
        print("= Links search start =")
        print(f"= {page} page search =")

        scrapper = DataScrapper()
        links = scrapper.links(page)

        if not links:
            self.PAGES_END_FLAG = True
            print("= Pages ended =")
            return
        for link in links:
            car = scrapper.page_processing(link)
            self.cars[car.url] = car
            thread = threading.current_thread()
            name = thread.name
            print(f"In thread {name}: {car.url}")

            time.sleep(0.1)

        print(f"= {page} page ended =")
        return True


if __name__ == "__main__":
    bot = Bot()
    bot.run()