
#  * https://auto.ria.com/uk/search/page=0&size=10
#  ? <section class="ticket-item" data-advertisement-id="35913460" data-user-id="13762872" data-search-position="1">  
#  * data-search-position does not become 1 on next page
#  ? <div class="hide" data-link-to-view="/auto_land_rover_range_rover_35913460.html">

import requests
from bs4 import BeautifulSoup
from modules.car import CarInfo


URL_BASE = "https://auto.ria.com/uk"


# *LINKS SEARCH

URL_SEARCH = "/car/used/?page=5"
page = requests.get(URL_BASE + URL_SEARCH)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("section", class_="ticket-item")
#  print(len(results))

for result in results:
    div = result.find("div", class_="hide")
    link = div.get("data-link-to-view")


# *PAGE SCRRAP
link = "/auto_honda_ens1_35917839.html"
link = "/auto_mercedes_benz_s_class_35764694.html"
page = requests.get(URL_BASE + link)

soup = BeautifulSoup(page.content, "html.parser")

car = {}
car["url"] = link
car["title"] = soup.find("h1", class_="head").text.strip()

price = soup.find("div", class_="price_value").find('strong')
price = price.text[:-2].replace(' ', '')
car["price_usd"] = int(price)


odometer = soup.find("div", class_="base-information bold").find(class_="size18")
odometer = int(f"{odometer.text.strip()}000")
car["odometer"] = odometer

car["username"] = soup.find(class_="seller_info_name").text.strip()

#  !PhoneNumber
car["phone_number"] = ''

image_url = soup.find("div", class_="photo-620x465").find("img").attrs["src"]
car["image_url"] = image_url

image_count = soup.find(class_="count-photo").find(class_="mhide")
image_count = int(image_count.text[2:].strip())
car["image_count"] = image_count

if soup.find("span", class_="state-num"):
    car["car_number"] = soup.find("span", class_="state-num").contents[0].strip()
else:
    car["car_number"] = None

if soup.find(class_="label-vin"):
    car["car_vin"] = soup.find(class_="label-vin").text.strip()
else:
    car["car_vin"] = soup.find(class_="vin-code").text.strip()

print(car)
