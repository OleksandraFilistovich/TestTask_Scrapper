import time
import random
import threading

from app.modules.scrapper import DataScrapper

PAGE_START = 1
PAGES_END_FLAG = False


class Bot:
    def __init__(self):
        self.threads_list: list[threading.Thread] = []
        self.max_threads = 5
        self.flags_for_stop = {}
        self.page = PAGE_START
        self.pages_end = False

    def clear_threads(self):
        for thread in self.threads_list[:]:
            if not thread.is_alive():
                self.threads_list.remove(thread)
    
    def run(self):
        while not PAGES_END_FLAG:
            
            self.clear_threads()
            
            for i in range(self.max_threads):
                
                x = threading.Thread(target=collecting_info, name=f'Thread {self.page}', daemon=True, args=(self.page,))
                print(f"=== {x.name} ===")
                self.page += 1

                x.start()
                self.threads_list.append(x)

            for thread in self.threads_list:

                thread.join()


def collecting_info(page: int):
    """Goes through found car pages in bunches,
    prints car info if possible,
    then goes to find more on next page."""
    print("= Links search start =")
    print(f"= {page} page search =")

    scrapper = DataScrapper()
    links = scrapper.links(page)

    if not links:
        PAGES_END_FLAG = True
        print("= Pages ended =")
        return 
    for link in links:
        car = scrapper.page_processing(link)

        thread = threading.current_thread()
        name = thread.name
        print(f"In thread {name}: {car.url}")

        time.sleep(0.1)

    print(f"= {page} page ended =")
    return True


if __name__ == "__main__":
    bot = Bot()
    bot.run()
