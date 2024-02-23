from m_worker.worker import Worker
from database.database_layer import CarsDB,TasksDB
from utils.car import CarInfo

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

# ?TEST CODE
tasks_db.populate(2,6)
print(tasks_db.tasks_take())

class Orchestrator:
    def __init__(self) -> None:
        pass
        #w = Worker()
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


