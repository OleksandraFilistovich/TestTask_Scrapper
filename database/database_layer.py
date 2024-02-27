import sqlalchemy as sq
from sqlalchemy.orm import Session

from utils.car import CarInfo
from utils.logs import get_logger
from database.models import Base, Cars, Tasks


LOGGER = get_logger('DB')

class TableDB:
    def __init__(self, user, password, host, port, name) -> None:
        """Connect to database and create tables if they don't exist"""
        self.engine = sq.create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}",
        )
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

        LOGGER.info('Engine is running')
    

class CarsDB(TableDB):
    """Class to work with 'Cars' table."""

    def bulk_insert(self, list_values: list[CarInfo]) -> None:
        """
        Inserts info from list of car into table if possible.
        Writes exact exception if failed.
        """
        with self.engine.connect() as conn:
            for value in list_values:
                try:
                    conn.execute(Cars.__table__.insert(), value)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    LOGGER.error("Can't insert value to Cars table! {e}")
                else:
                    LOGGER.success(f'Data added to Cars DB')
    
    #!FIX
    def cars_take(self) -> list:
        """Returns list of cars saved in table."""
        cars = self.session.query(Cars).all()
        return [cars.__dict__['title'] for car in cars]

class TasksDB(TableDB):
    """Class to work with 'Tasks' table."""

    def populate(self, start_page: int, end_page: int) -> None:
        """Adds pages numbers as tasks to table."""
        with self.engine.connect() as conn:
            for page in range(start_page, end_page+1):
                value = {'page_number' : page}
                try:
                    conn.execute(Tasks.__table__.insert(), value)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    LOGGER.error("Can't insert value to Tasks table! {e}")
                else:
                    LOGGER.success(f'Tasks successfully added to DB.')
    
    def tasks_take(self) -> list:
        """Returns all not completed tasks."""
        tasks = self.session.query(Tasks).where(Tasks.is_complete == False).all()
        return [task.__dict__['page_number'] for task in tasks]
