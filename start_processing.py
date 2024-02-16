import time
import multiprocessing

from app.modules.scrapper import DataScrapper

PAGE_START = 1


class Bot:
    def __init__(self):
        self.process_list: list[multiprocessing.Process] = []
        self.max_processes = 5
        self.page = PAGE_START
        self.PAGES_END_FLAG = multiprocessing.Queue()
        self.cars_queue = multiprocessing.Queue()
        self.cars: list = []


    def clear_processes(self):
        for process in self.process_list[:]:
            if not process.is_alive():
                self.process_list.remove(process)

    def bulk_save(self):
        for i in iter(self.cars_queue.get, 'STOP'):
            self.cars.append(i)
            return len(self.cars)

    def run(self):
        while self.PAGES_END_FLAG.empty():

            self.clear_processes()
            
            while True:
                if len(self.process_list) < self.max_processes:
                    break
                self.clear_processes()
                print(self.bulk_save())
                time.sleep(0.1)

            x = multiprocessing.Process(target=self.collecting_info, daemon=True, name=f'Process {self.page}', args=(self.page,))
            x.start()

            print(f"=== {x.name} ===")
            self.page += 1

            self.process_list.append(x)

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
            self.PAGES_END_FLAG.put(True)
            print("= Pages ended =")

            return
        for link in links:
            car = scrapper.page_processing(link)
            self.cars_queue.put(car)

            process = multiprocessing.current_process()
            name = process.name
            print(f"In process {name}: {car.url}")

            time.sleep(0.1)

        print(f"= {page} page ended =")
        return True


if __name__ == "__main__":
    bot = Bot()
    bot.run()
