import asyncio

from database.database_layer import CarsDB,TasksDB
from utils.car import CarInfo
from utils.rs import Cache_Tasks

import os


name_db = os.environ.get("POSTGRES_DB")
user_db = os.environ.get("POSTGRES_USER")
password_db = os.environ.get("POSTGRES_PASSWORD")
host_db = os.environ.get("POSTGRES_HOST")
port_db = os.environ.get("POSTGRES_PORT")

host_rs = os.environ.get("REDIS_HOST")
port_rs = os.environ.get("REDIS_PORT")
number_db_rs = os.environ.get("REDIS_DATABASES")
password_rs = os.environ.get("REDIS_PASSWORD")


#  *Connection to DB tables
cars_db = CarsDB(user_db, password_db, host_db, port_db, name_db)
tasks_db = TasksDB(user_db, password_db, host_db, port_db, name_db)

#  *Connection to redis
CACHE = Cache_Tasks()

#  *Creates tasks inside Tasks table
tasks_db.populate(1,2)


class Orchestrator:
    """
    Class cycles and operates data, takes from, saves to DB.
    Stores tasks in redis for worker to see.
    """

    async def run(self) -> None:
        while True:
            #  *Takes not done tasks from Tasks table
            tasks_to_redis = tasks_db.tasks_take()
            #  *Adds tasks for worker to work on
            CACHE.add_tasks(tasks_to_redis)
            
            await asyncio.sleep(5)

            #  *Takes results and stores them inside DB
            #  ?break for testing, real orchestrator runs indefinitely
            results_to_db = CACHE.get_results()
            if len(results_to_db) < 10:
                continue
            else:
                print(len(results_to_db))
                cars_db.bulk_insert(list(results_to_db.values()))
                break

        print("ORCHESTRATOR STOPPED")
