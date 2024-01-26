import requests
from bs4 import BeautifulSoup

from modules.car import CarInfo

URL_BASE = "https://auto.ria.com/uk"
URL_SEARCH = "/car/used/?page="


def links_search(page_number: int) -> list[str]:
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


def page_processing(url: str) -> CarInfo:
    """Collects data of the car.
    Returns it as CarInfo type."""
    page = requests.get(URL_BASE + url)
    soup = BeautifulSoup(page.content, "html.parser")

    car = CarInfo()

    car.url = url

    car.title = soup.find("h1", class_="head").text.strip()

    price = soup.find("div", class_="price_value").find("strong")
    res = "".join([elem for elem in price.text if elem.isdigit()]) 
    car.price_usd = int(res.strip())

    odometer = soup.find("div", class_="base-information bold").find(class_="size18")
    if odometer:
        odometer = int(f"{odometer.text.strip()}000")
    car.odometer = odometer

    username = soup.find(class_="seller_info_name")
    if username:
        car.username = username.text.strip()

    #  !PhoneNumber
    car.phone_number = ""

    image_url = soup.find("div", class_="photo-620x465").find("img")
    if image_url:
        image_url = image_url.attrs["src"]
    car.image_url = image_url

    image_count = soup.find(class_="count-photo").find(class_="mhide")
    if image_count:
        image_count = int(image_count.text[2:].strip())
    car.image_count = image_count

    car_number = soup.find("span", class_="state-num")
    if car_number:
        car.car_number = car_number.contents[0].strip()

    if soup.find(class_="label-vin"):
        car.car_vin = soup.find(class_="label-vin").text.strip()
    elif soup.find(class_="vin-code"):
        car.car_vin = soup.find(class_="vin-code").text.strip()

    return car
