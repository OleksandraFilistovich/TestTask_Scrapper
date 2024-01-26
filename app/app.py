import os

from modules.database import CarsDB
from modules.scrapper import links_search, page_processing

name = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
port = os.environ.get("POSTGRES_PORT")


#  Writes car info to db if possible
def write_value(car_info):
    print("= Write start =")
    db.insert_value(car_info)


def collecting_info(starting_page: int):
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
            write_value(car)

        print(f"= {page} page search =")
        links = links_search(page)
        page += 1

        for link in links:
            car = page_processing(link)
            write_value(car)
    print("= Pages ended =")


if __name__ == "__main__":
    print("= Application started =")

    #  Connect to the database
    db = CarsDB.create_connection(user, password, host, port, name)

    collecting_info(int(os.environ.get("STARTING_PAGE")))
