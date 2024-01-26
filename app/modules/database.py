from sqlalchemy import String, Integer, Column
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import DeclarativeBase

from modules.car import CarInfo


class Base(DeclarativeBase):
    pass


class Cars(Base):
    """Database table 'Cars' representation."""
    __table__ = Table(
        "cars",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("url", String),
        Column("title", String),
        Column("price_usd", Integer),
        Column("odometer", Integer),
        Column("username", String),
        Column("phone_number", String),
        Column("image_url", String),
        Column("images_count", Integer),
        Column("car_number", String),
        Column("car_vin", String),
        Column("datetime_found", String)
    )


class CarsDB():
    """Class to work with 'Cars' db."""
    __instance = None

    def __init__(self, user, password, host, port, name):
        """Singleton class."""
        if CarsDB.__instance is not None:
            raise Exception(
                "This class is a singleton, use CarsDB.create_connection()")
        else:
            CarsDB.__instance = self
            db_connect = f"postgresql://{user}:{password}@{host}:{port}/{name}"
            self.engine = create_engine(db_connect)

            print("= Engine is running =")

    @staticmethod
    def create_connection(user, password, host, port, name):
        """For DB initiation in main code. Instance creation."""
        if CarsDB.__instance is None:
            CarsDB.__instance = CarsDB(user, password, host, port, name)

        return CarsDB.__instance
    
    def insert_value(self, value:CarInfo) -> None:
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
