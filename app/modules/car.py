from pprint import pformat

from dataclasses import dataclass, asdict


@dataclass
class CarInfo:
    """Class for storing fetched car information."""
    url: str
    title: str
    price_usd: int
    odometer: int
    username: str
    phone_number: str
    image_url: str
    images_count: int
    car_number: str
    car_vin: str

    def to_dict(self):
        return asdict(self)
    
    def __repr__(self):
        return pformat(asdict(self))
