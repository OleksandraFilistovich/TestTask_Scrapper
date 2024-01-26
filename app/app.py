import time
import os

from sqlalchemy import create_engine, text, select


db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('POSTGRES_HOST')
db_port = os.environ.get('POSTGRES_PORT')

# Connecto to the database
db_string = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
db = create_engine(db_string)

def add_new_row(n):
    with db.connect() as conn:
        query = f"""INSERT INTO cars (url) VALUES ({n});"""
        result = conn.execute(text(query))
        conn.commit()


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
