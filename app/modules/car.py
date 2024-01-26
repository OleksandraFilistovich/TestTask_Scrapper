from pprint import pformat

from dataclasses import dataclass, asdict


@dataclass
class CarInfo:
    """Class for storing fetched car information."""
    url: str = None
    title: str = None
    price_usd: int = None
    odometer: int = None
    username: str = None
    phone_number: str = None
    image_url: str = None
    images_count: int = None
    car_number: str = None
    car_vin: str = None

    def to_dict(self):
        return asdict(self)
    
    def __repr__(self):
        return pformat(asdict(self))
