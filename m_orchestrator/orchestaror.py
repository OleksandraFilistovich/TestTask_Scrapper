import os
import asyncio

from utils.rs import Cache
from utils.logs import get_logger
from database.database_layer import CarsDB,TasksDB
from database.database_layer_mongo import CarsDB as MongoCarsDB
from database.database_layer_mongo import TasksDB as MongoTasksDB


#'mongo' or 'postgres'
DATABASE = 'mongo'

LOGGER = get_logger("Orchestrator")

#  *Connection to DB tables
if DATABASE == 'postgres':
    name_db = os.environ.get("POSTGRES_DB")
    user_db = os.environ.get("POSTGRES_USER")
    password_db = os.environ.get("POSTGRES_PASSWORD")
    host_db = os.environ.get("POSTGRES_HOST")
    port_db = os.environ.get("POSTGRES_PORT")

    cars_db = CarsDB(user_db, password_db,
                     host_db, port_db, name_db)
    tasks_db = TasksDB(user_db, password_db,
                       host_db, port_db, name_db)
elif DATABASE == 'mongo':
    cars_db = MongoCarsDB()
    tasks_db = MongoTasksDB()

#  *Connection to redis
host_rs = os.environ.get("REDIS_HOST")
port_rs = os.environ.get("REDIS_PORT")
number_db_rs = os.environ.get("REDIS_DATABASES")
password_rs = os.environ.get("REDIS_PASSWORD")

cache_0 = Cache(0)
cache_1 = Cache(1)

#  *Creates tasks inside Tasks table
tasks_db.populate_tasks(1,2)


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
            cache_0.add_tasks(tasks_to_redis)
            
            await asyncio.sleep(5)

            #  *Takes results and stores them inside DB
            #  ?break for testing, real orchestrator runs indefinitely
            results_to_db = cache_1.get_results()
            if len(results_to_db) < 10:
                continue
            else:
                LOGGER.info(f'Collected {len(results_to_db)} cars info.')
                cars_db.bulk_insert(results_to_db)
                break

        LOGGER.info('Orchestrator stopped.')
