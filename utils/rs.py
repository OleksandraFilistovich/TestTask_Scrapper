import redis
from datetime import datetime


host_rs = 'redis'
port_rs = 6379
password_rs = ''

# ?TEST DATA
car_example = {'car_number': 'None',
               'car_vin': 'WVGZZZ5NZKM029545',
               'image_url': 'https://cdn3.jpg',
               'images_count': '196',
               'odometer': 240000,
               'phone_number': '(067) 314 04 36',
               'price_usd': '25700',
               'title': ' Volkswagen',
               'url': 'https://auto.ria.com/',
               'username': 'Сергій'}


class Cache:
    def __init__(self, number_db: int, host: str = host_rs, port: int = port_rs, password: str = password_rs):
        self.red = redis.Redis(host=host, port=port, db=number_db, password=password, decode_responses=True)
        self.pipeline = self.red.pipeline()

class Cache_Tasks:
    def __init__(self, host: str = host_rs, port: int = port_rs, password: str = password_rs):
        self.tasks = redis.Redis(host=host, port=port, db=0, password=password, decode_responses=True)
        self.results = redis.Redis(host=host, port=port, db=1, password=password, decode_responses=True)
    
    def add_tasks(self, tasks: list[int]) -> None:
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
        self.tasks.set(task, str(datetime.now()))

    def clean_tasks(self) -> None:
        keys = self.tasks.keys()

        for key in keys:
            self.tasks.delete(key)

    def add_result(self, task: int, car: dict) -> None:
        for key in car.keys():
            self.results.hset(name=task, key=key, value=car[key])
        self.tasks.delete(task)
    
    def add_results(self, task: int, cars: list[dict]) -> None:
        ind = 0
        for car in cars:
            ind += 1
            for key in car.keys():
                name = f'{task}-{ind}'
                self.results.hset(name=name, key=key, value=car[key])
        #self.tasks.delete(task)
    
    def get_results(self) -> dict:
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



# ?TEST FUNCTION
def cache_func():

    cache = Cache_Tasks()
    cache.clean_tasks()

    cache.add_tasks([1,2,30,4,5])
    print(cache.get_tasks())
    #cache.update_task(2)
    print(cache.get_tasks())
    
    #cache.clean_tasks()
    #print(cache.get_tasks())
    
    cache.add_results(2,[car_example,car_example])
    cache.add_results(30,[car_example,car_example])
    print(cache.get_results())
    print(cache.get_results())
    print(cache.get_tasks())

#cache_func()



def main():
    cache_0 = Cache(0)
    cache_1 = Cache(1)
    cache_2 = Cache(2)

    cache_0.red.set('a', 'aa')
    cache_0.red.set('b', '')
    cache_0.red.set('b', 'bb')

    keys = cache_0.red.keys()
    #print(keys)

    for key in keys:
        value = cache_0.red.get(key)
        print(key, value)
    
    keys = cache_0.red.keys()
    print(keys)

    #await cache_2.red.incrby('foo', 1)
    #print(await cache_2.get('foo'))

#main()