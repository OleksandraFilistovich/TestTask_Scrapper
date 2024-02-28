from pymongo import MongoClient
from utils.logs import get_logger


LOGGER = get_logger('DB')

class MongoDB:
    def __init__(self, host: str = "mongodb", port: int = 27017):
        self.myclient = MongoClient(host, port)
        self.mydb = self.myclient["mydatabase"]

        LOGGER.info('Engine is running')


class CarsDB(MongoDB):
    def __init__(self) -> None:
        super().__init__()

        self.cars = self.mydb["cars"]
        self.cars.create_index("url", unique=True)

        self.cars.delete_many({})
    
    def bulk_insert(self, cars_values: dict) -> None:
        cars_values = list(cars_values.values())

        for value in cars_values:
            try:
                self.cars.insert_one(value)
            except Exception as e:
                LOGGER.error("Can't insert value to Cars table! {e}")
            else:
                LOGGER.success(f'Data added to Cars DB')
    
    def take_cars(self) -> list:
        return [car for car in self.cars.find()]
    
    def delete_all(self) -> None:
        self.cars.delete_many({})


class TasksDB(MongoDB):
    def __init__(self) -> None:
        super().__init__()
        
        self.tasks = self.mydb["tasks"]
        self.tasks.create_index("page_number", unique=True)

        self.tasks.delete_many({})

    def populate_tasks(self, start_page: int, end_page: int) -> None:
        for page in range(start_page, end_page+1):
            task = {}
            task['page_number'] = page
            task['in_progress'] = False
            task['is_complete'] = False

            try:
                self.tasks.insert_one(task)
            except Exception as e:
                LOGGER.error("Can't insert value to Tasks table! {e}")
            else:
                LOGGER.success(f'Tasks successfully added to DB.')
    
    def tasks_take(self) -> list:
        tasks_to_do = self.tasks.find({"is_complete": False})
        return [task['page_number'] for task in tasks_to_do]
    
    def delete_all(self) -> None:
        self.tasks.delete_many({})
