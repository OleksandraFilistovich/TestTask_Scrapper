import redis
from datetime import datetime


host_rs = 'redis'
port_rs = 6379
password_rs = ''


class Cache:
    """Redis connection. Methods to work with redis cache."""
    def __init__(self, number_db: int, host: str = host_rs,
                 port: int = port_rs, password: str = password_rs) -> None:
        
        self.red = redis.Redis(host=host, port=port, db=number_db,
                               password=password, decode_responses=True)
        self.pipeline = self.red.pipeline()

    def add_tasks(self, tasks: list[int]) -> None:
        """Adds given tasks to queue."""
        for task in tasks:
            self.pipeline.lpush('queue_tasks', task)
        self.pipeline.execute()
    
    def get_tasks(self, amount: int) -> list[str]:
        """Returns set amount of tasks."""
        tasks = self.red.rpop(name='queue_tasks', count=amount)
        return tasks
    
    def add_results(self, task: int, cars: list[dict]) -> None:
        """Stores cars info. Key is '{page_number}-{car_index}'."""
        ind = 0
        for car in cars:
            ind += 1
            for key in car.keys():
                name = f'{task}-{ind}'
                self.pipeline.hset(name=name, key=key, value=car[key])
        self.pipeline.execute()
    
    def get_results(self) -> dict:
        """
        Returns all stored cars data in dict {index:car_info_as_dict}.
        Deletes all tasks from which cars been collected.
        """
        results = {}
        cars = self.red.keys()

        for car in cars:
            results[car] = {}
            keys =  self.red.hkeys(car)
            
            for key in keys:
                results[car][key] = self.red.hget(car, key)
            self.pipeline.delete(car)

        self.pipeline.execute()        
        return results


class Cache_Tasks:
    """Redis db to store tasks and their results."""

    def __init__(self, host: str = host_rs,
                 port: int = port_rs, password: str = password_rs) -> None:
        """Initialize connection to dbs for tasks and results."""
        self.tasks = redis.Redis(host=host, port=port, db=0,
                                 password=password, decode_responses=True)
        self.results = redis.Redis(host=host, port=port, db=1,
                                   password=password, decode_responses=True)
    
    def add_tasks(self, tasks: list[int]) -> None:
        """Adds given tasks to store."""
        for task in tasks:
            self.tasks.set(task, '')
    
    def get_tasks(self) -> list:
        """Returns not started tasks."""
        tasks = []
        keys = self.tasks.keys()

        for key in keys:
            value = self.tasks.get(key)
            if not value:
                tasks.append(key)
        return tasks
    
    def update_task(self, task: int) -> None:
        """Update task with 'started at' timestamp."""
        self.tasks.set(task, str(datetime.now()))

    def clean_tasks(self) -> None:
        """Delete ALL tasks."""
        keys = self.tasks.keys()

        for key in keys:
            self.tasks.delete(key)
    
    def add_results(self, task: int, cars: list[dict]) -> None:
        """Stores cars info. Key is '{page_number}-{car_index}'."""
        ind = 0
        for car in cars:
            ind += 1
            for key in car.keys():
                name = f'{task}-{ind}'
                self.results.hset(name=name, key=key, value=car[key])
        #self.tasks.delete(task)
    
    def get_results(self) -> dict:
        """
        Returns all stored cars data in dict {index:car_info_as_dict}.
        Deletes all tasks from which cars been collected.
        """
        results = {}
        cars = self.results.keys()
        tasks_nums = set([car[:car.index('-')] for car in cars])

        for car in cars:
            results[car] = {}
            keys =  self.results.hkeys(car)
            
            for key in keys:
                results[car][key] = self.results.hget(car, key)
            self.results.delete(car)
            
        for task in tasks_nums:
            self.tasks.delete(task)
        
        return results
