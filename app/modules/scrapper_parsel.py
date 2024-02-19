from playwright.sync_api import sync_playwright
from parsel import Selector

from .car import CarInfo

URL_BASE = "https://auto.ria.com/uk"
URL_SEARCH = "/car/used/?page="


class DataScrapperParsel:

    def __init__(self, browser_page) -> None:
        self.browser_page = browser_page

    def get_html(self, url: str):
        """Get HTML from given url."""

        self.browser_page.goto(url)
        html_content = self.browser_page.content()

        return html_content
    
    def collect_links(self, page_num: int) -> list[str]:
        """Returns links to pages with cars."""

        url_to_search = URL_SEARCH + str(page_num)

        html_content = self.get_html(URL_BASE + url_to_search)
        selector = Selector(text=html_content)

        xpath_query = '//a[@class="m-link-ticket"]/@href'
        links = selector.xpath(xpath_query).getall()

        return links
    
    @staticmethod
    def _price(selector: Selector) -> int:
        price = selector.xpath('//div[@class="price_value"]/strong/text()')
        price = "".join([elem for elem in price.get() if elem.isdigit()])
        return price
    
    @staticmethod
    def _odometer(selector: Selector) -> int:
        xpath = '//div[@class="base-information bold"]/span[@class="size18"]/text()'
        odometer = selector.xpath(xpath).get()
        if odometer:
            odometer = int(f"{odometer.strip()}000")
        return odometer

    @staticmethod
    def _username(selector: Selector) -> str:
        xpath = '//div[contains(@class, "seller_info_name bold")]/text()'
        name = selector.xpath(xpath).get()

        if not name:
            xpath = '//h4[@class="seller_info_name"]/a/text()'
            name = selector.xpath(xpath).get()
        
        if not name:
            return ''
        
        return name.strip()
    
    def _phone_number(self) -> str:
        button = self.browser_page.get_by_role("link")
        button.get_by_text("показати").nth(0).click()

        class_name = '.popup-successful-call-desk'
        phone_number = self.browser_page.query_selector(class_name)

        return phone_number.text_content()
    
    @staticmethod
    def _image_url(selector: Selector) -> str:
        xpath = '//img[@class="outline m-auto"]/@src'
        url = selector.xpath(xpath).get()
        return url
    
    @staticmethod
    def _image_count(selector: Selector) -> str:
        xpath = '//span[@class="count"]/span[@class="mhide"]/text()'
        count = selector.xpath(xpath).get()[2:]
        return count
    
    @staticmethod
    def _car_number(selector: Selector) -> str:
        xpath = '//span[@class="state-num ua"]/text()'
        number = selector.xpath(xpath).get()
        return number
    
    @staticmethod
    def _car_vin(selector: Selector) -> str:
        xpath = '//span[@class="label-vin" or @class="vin-code"]/text()'
        vin = selector.xpath(xpath).get()
        return vin

    def collecting_data(self, url: str):
        """Collecting car data from page."""

        car = CarInfo()
        html_content = self.get_html(url)
        selector = Selector(text=html_content)

        car.url = url
        car.title = selector.xpath('//h1[@class="head"]/text()').get()

        car.price_usd = self._price(selector)
        car.odometer = self._odometer(selector)
        car.username = self._username(selector)
        car.phone_number = self._phone_number()
        car.image_url = self._image_url(selector)
        car.images_count = self._image_count(selector)
        car.car_number = self._car_number(selector)
        car.car_vin = self._car_vin(selector)

        return car
