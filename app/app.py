import time
import random

from sqlalchemy import create_engine, text, select

db_name = 'database'
db_user = 'username'
db_pass = 'password'
db_host = 'db'
db_port = '5432'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

def add_new_row(n):
    with db.connect() as conn:
        query = f"""INSERT INTO cars (url) VALUES ({n});"""
        result = conn.execute(text(query))
        conn.commit()
        print(f"===RESULT==={result}")


def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    with db.connect() as conn:
        query = """SELECT * FROM cars"""

        for result in conn.execute(text(query)):  
            print(result)


if __name__ == '__main__':
    print('== Application started..')
    
    k = 0
    while True:
        time.sleep(5)
        k += 1
        add_new_row(k)
        print('The last value insterted is: {}'.format(get_last_row()))
