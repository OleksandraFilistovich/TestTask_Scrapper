import sqlalchemy as sq
from sqlalchemy.orm import Session
from database.models import Base, Cars, Tasks

from utils.car import CarInfo


class TableDB:
    def __init__(self, user, password, host, port, name) -> None:
        """Connect to database and create tables if they don't exist"""
        self.engine = sq.create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}",
        )
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

        print("= Engine is running =")
    

class CarsDB(TableDB):
    """Class to work with 'Cars' table."""
    __instance = None
    
    #  ?bulk can be used instead
    def insert_value(self, value: CarInfo) -> None:
        """Inserts info of the car into table if possible.
        Writes exact exception if failed."""
        with self.engine.connect() as conn:
            try:
                conn.execute(Cars.__table__.insert(), value.to_dict())
                conn.commit()
                print("= Data successfully added =")
                print(value.to_dict())
            except Exception as e:
                conn.rollback()
                print(f"! Can't insert value.! {e}")
    
    def bulk_insert(self, list_values: list[CarInfo]) -> None:
        """Inserts info from list of car into table if possible.
        Writes exact exception if failed."""
        with self.engine.connect() as conn:
            for value in list_values:
                try:
                    conn.execute(Cars.__table__.insert(), value)
                    conn.commit()
                    print("= Data successfully added =")
                    print(value)
                except Exception as e:
                    conn.rollback()
                    print(f"! Can't insert value.! {e}")
    
    #!FIX
    def cars_take(self) -> list:
        cars = self.session.query(Cars).all()
        return [cars.__dict__['title'] for car in cars]

class TasksDB(TableDB):
    """Class to work with 'Tasks' table."""
    __instance = None
    
    def populate(self, start_page: int, end_page: int) -> None:

        with self.engine.connect() as conn:
            for page in range(start_page, end_page+1):
                value = {'page_number' : page}
                try:
                    conn.execute(Tasks.__table__.insert(), value)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"! Can't insert value.! {e}")
            print(f"= Tasks successfully added to db =")
    
    def tasks_take(self) -> list:
        tasks = self.session.query(Tasks).where(Tasks.is_complete == False).all()
        return [task.__dict__['page_number'] for task in tasks]
