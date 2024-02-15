import requests
from bs4 import BeautifulSoup

from modules.car import CarInfo

URL_BASE = "https://auto.ria.com/uk"
URL_SEARCH = "/car/used/?page="


class DataScrapper:

    def links(self, page_number: int) -> list[str]:
        """Goes through the page with advertisments.
        Collects and returns links to the pages with cars in them."""

        links = []
        url_to_search = URL_SEARCH + str(page_number)

        page = requests.get(URL_BASE + url_to_search)
        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find_all("section", class_="ticket-item")

        if len(results) == 0:
            return None

        for result in results:
            div = result.find("div", class_="hide")
            links.append(div.get("data-link-to-view"))
        return links

    @staticmethod
    def _price(soup_data) -> int:
        price = soup_data.find("div", class_="price_value").find("strong")
        res = "".join([elem for elem in price.text if elem.isdigit()]) 
        return int(res.strip())
    
    @staticmethod
    def _odometer(soup_data) -> int:
        odometer = soup_data.find("div", class_="base-information bold")
        odometer = odometer.find(class_="size18")
        if odometer:
            odometer = int(f"{odometer.text.strip()}000")
        return odometer
    
    @staticmethod
    def _username(soup_data) -> str:
        username = soup_data.find(class_="seller_info_name")
        if username:
            return username.text.strip()

    @staticmethod
    def _image_url(soup_data) -> str:
        image_url = soup_data.find("div", class_="photo-620x465").find("img")
        if image_url:
            image_url = image_url.attrs["src"]
        return image_url
    
    @staticmethod
    def _image_count(soup_data) -> int:
        image_count = soup_data.find(class_="count-photo")
        image_count = image_count.find(class_="mhide")
        if image_count:
            image_count = int(image_count.text[2:].strip())
        return image_count
    
    @staticmethod
    def _car_number(soup_data) -> str:
        car_number = soup_data.find("span", class_="state-num")
        if car_number:
            return car_number.contents[0].strip()
    
    @staticmethod
    def _car_vin(soup_data) -> str:
        if soup_data.find(class_="label-vin"):
            return soup_data.find(class_="label-vin").text.strip()
        elif soup_data.find(class_="vin-code"):
            return soup_data.find(class_="vin-code").text.strip()

    def page_processing(self, url: str) -> CarInfo:
        """Collects data of the car.
        Returns it as CarInfo type."""

        page = requests.get(URL_BASE + url)
        soup = BeautifulSoup(page.content, "html.parser")

        car = CarInfo()

        car.url = url
        car.title = soup.find("h1", class_="head").text.strip()

        car.price_usd = self._price(soup)
        car.odometer = self._odometer(soup)
        car.username = self._username(soup)

        #  !PhoneNumber
        car.phone_number = ""

        car.image_url = self._image_url(soup)
        car.image_count = self._image_count(soup)
        car.car_number = self._car_number(soup)
        car.car_vin = self._car_vin(soup)

        return car
