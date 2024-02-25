import asyncio
from playwright.async_api import async_playwright, BrowserContext

from m_worker.worker import Worker
from database.database_layer import CarsDB,TasksDB
from utils.car import CarInfo
from utils.rs import Cache_Tasks

import os

#id page_number in_progress is_complete
# ?TEST DATA
car_example = {'car_number': '',
               'car_vin': 'WVGZZZ5NZKM029545',
               'image_url': 'https://cdn3.jpg',
               'images_count': '196',
               'odometer': 240000,
               'phone_number': '(067) 314 04 36',
               'price_usd': '25700',
               'title': ' Volkswagen',
               'url': 'https://auto.ria.com/',
               'username': 'Сергій'}

name_db = os.environ.get("POSTGRES_DB")
user_db = os.environ.get("POSTGRES_USER")
password_db = os.environ.get("POSTGRES_PASSWORD")
host_db = os.environ.get("POSTGRES_HOST")
port_db = os.environ.get("POSTGRES_PORT")

host_rs = os.environ.get("REDIS_HOST")
port_rs = os.environ.get("REDIS_PORT")
number_db_rs = os.environ.get("REDIS_DATABASES")
password_rs = os.environ.get("REDIS_PASSWORD")


cars_db = CarsDB(user_db, password_db, host_db, port_db, name_db)
tasks_db = TasksDB(user_db, password_db, host_db, port_db, name_db)

cache = Cache_Tasks()


class Orchestrator:
    def __init__(self) -> None:
        self.tasks_list = []
        self.max_tasks = 3
        self.cars_done = []
        #print("Orchestrator created.")
    
    def reset_tasks(self):
        pass

    def plan_tasks(self):
        pass

    def update_tasks(self):
        pass

    def take_results(self):
        pass

    def bulk_save(self, list_values: list[CarInfo] = []):

        print("Start bulk")
        list_values.append(car_example.copy())
        car_example['url'] = car_example['url'] + '1'
        list_values.append(car_example.copy())
        car_example['url'] = car_example['url'] + '2'
        list_values.append(car_example.copy())
        car_example['url'] = car_example['url'] + '3'
        list_values.append(car_example.copy())

        cars_db.bulk_insert(list_values)
    
    def clear_tasks(self):
        for task in self.tasks_list[:]:
            if task.done():
                self.tasks_list.remove(task)

    async def run_worker(self, context : BrowserContext, page_num: str):
        while len(self.tasks_list) >= self.max_tasks:
            self.clear_tasks()
            await asyncio.sleep(0.01)

        worker = Worker(page_num)
        print(f'create worker {page_num}')

        browser_page = await context.new_page()

        task = asyncio.create_task(worker.collecting_info(browser_page,
                                                          cache))
        self.tasks_list.append(task)

    async def run(self):
        #  *Creates tasks inside Tasks table
        tasks_db.populate(1,2)
        #  *Takes not done tasks from Tasks table
        tasks_to_redis = tasks_db.tasks_take()
        #  *Adds tasks to work on
        cache.add_tasks(tasks_to_redis)
        #  *Takes not done tasks from redis
        tasks_to_do = cache.get_tasks()
        
        print(tasks_to_do)

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            
            for task in tasks_to_do:
                pass
                await self.run_worker(context, task)
            
            while len(self.tasks_list) > 0:
                self.clear_tasks()
                await asyncio.sleep(0.01)
        
        results_to_db = cache.get_results()
        print(results_to_db)

        cars_db.bulk_insert(list(results_to_db.values()))

        #db read needs fix
        #print(cars_db.cars_take())

        await browser.close()
