import time
import os

from modules.database import CarsDB
from modules.car import CarInfo


name = os.environ.get('POSTGRES_DB')
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')
port = os.environ.get('POSTGRES_PORT')

# Connecto to the database
db = CarsDB.create_connection(user, password, host, port, name)


def write_value(car_info):
    print("= Write start =")
    db.insert_value(car_info)


if __name__ == '__main__':
    print('= Application started =')
    
    k = 0
    while True:
        time.sleep(1)
        k += 1
        car_info = CarInfo('/auto.html', 'Benz', 16, 24, "Рома", "", "url_img", 33, "CA 3068 KC", 'WDDNG7DB3CA474969')
        write_value(car_info)
        #add_new_row(k)
        #print(get_last_row())
