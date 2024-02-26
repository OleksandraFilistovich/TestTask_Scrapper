import datetime
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Cars(Base):
    __tablename__ = "cars"
    id = sq.Column(sq.Integer, primary_key=True)

    url = sq.Column(sq.String(300), nullable=False, unique=True)
    title = sq.Column(sq.String(150))
    price_usd = sq.Column(sq.Integer)
    odometer = sq.Column(sq.Integer)
    username = sq.Column(sq.String(100))
    phone_number = sq.Column(sq.String(15))
    image_url = sq.Column(sq.String(300))
    images_count = sq.Column(sq.Integer)
    car_number = sq.Column(sq.String(10))
    car_vin = sq.Column(sq.String(17))
    datetime_found = sq.Column(sq.DateTime, default=datetime.datetime.utcnow)

class Tasks(Base):
    __tablename__ = "tasks"
    id = sq.Column(sq.Integer, primary_key=True)

    page_number = sq.Column(sq.Integer, unique=True)
    in_progress = sq.Column(sq.Boolean, default=False)
    is_complete = sq.Column(sq.Boolean, default=False)
