import os
import time
from datetime import datetime, timedelta

from modules.database import CarsDB
from modules.scrapper import links_search, page_processing


name = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
port = os.environ.get("POSTGRES_PORT")

env_hour = int(os.environ.get("APP_STARTING_HOUR"))
env_minutes = int(os.environ.get("APP_STARTING_MINUTE"))

starting_page = int(os.environ.get("STARTING_PAGE"))


def scrapper_start():
    #  Connect to the database
    db = CarsDB.create_connection(user, password, host, port, name)

    collecting_info(starting_page, db)

#  Writes car info to db if possible
def write_value(car_info, db):
    print("= Write start =")
    db.insert_value(car_info)


def collecting_info(starting_page: int, db):
    """Goes through found car pages in bunches,
    writes car info to db if possible,
    then goes to find more on next page."""
    print("= Links search start =")
    print(f"= {starting_page} page search =")

    links = links_search(starting_page)
    page = starting_page + 1

    while links:
        for link in links:
            car = page_processing(link)
            write_value(car, db)

        print(f"= {page} page search =")
        links = links_search(page)
        page += 1

    print("= Pages ended =")


if __name__ == "__main__":
    print("= Application started =")
    #  !Untimed start to test
    scrapper_start()

    #  Timed start
    delta = timedelta(days=1)

    now = datetime.now()
    needed_time = now.replace(hour=env_hour, minute=env_minutes, second=0)
    if now > needed_time:
        needed_time += delta

    while True:
        if datetime.now() >= needed_time:
            scrapper_start()
            needed_time += delta
        # Depending on need, check frequency can be changed
        print(f"= Waiting till {needed_time} =")
        print(f"Now {datetime.now()} ")
        time.sleep(10)

    





