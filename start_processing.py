import time
import multiprocessing

from app.modules.scrapper import DataScrapper

PAGE_START = 1


class Bot:
    def __init__(self):
        self.process_list: list[multiprocessing.Process] = []
        self.max_processes = 5
        self.flags_for_stop = {}
        self.page = PAGE_START
        #!
        self.pages_end = False
        self.PAGES_END_FLAG = False
        self.cars: list = {}

    def clear_processes(self):
        for process in self.process_list[:]:
            if not process.is_alive():
                self.process_list.remove(process)

    def bulk_save(self):
        pass

    def run(self):
        while not self.PAGES_END_FLAG:
            
            self.clear_processes()
            
            while True:
                if len(self.process_list) < self.max_processes:
                    break
                self.clear_processes()
                time.sleep(0.1)

            x = multiprocessing.Process(target=self.collecting_info, name=f'Process {self.page}', args=(self.page,))
            x.start()

            print(f"=== {x.name} ===")
            self.page += 1

            self.process_list.append(x)

            self.bulk_save()

        for process in self.process_list:
            process.join()

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
            process = multiprocessing.current_process()
            name = process.name
            print(f"In process {name}: {car.url}")

            time.sleep(0.1)

        print(f"= {page} page ended =")
        return True


if __name__ == "__main__":
    bot = Bot()
    bot.run()