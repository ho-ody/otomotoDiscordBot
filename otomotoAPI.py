import time

import requests
import html
import re

from Offer import Offer


def test():
    testurl1 = 'https://www.otomoto.pl/osobowe/audi/a3/rzeszow?search%5Bfilter_enum_fuel_type%5D=diesel&search%5Bdist%5D=200&search%5Bfilter_float_mileage%3Ato%5D=200000&search%5Bfilter_float_price%3Afrom%5D=15000&search%5Bfilter_float_price%3Ato%5D=20000&search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true'

    # This will yield only the HTML code
    url = testurl1
    response = requests.get(url)
    response_raw = html.unescape(response.text);
    #print(response.text)
    with open("response.txt", "wb") as file:
        file.write(response.content)

    s1 = time.time()
    extractOffersFromResponse(response_raw)
    print(f' @ extractOffersFromResponse took: {time.time()-s1:.3f}s')

def extractOffersFromResponse(response: str):
    starts_with = '<a href="https://www.otomoto.pl/oferta/'
    # find all text occurrences
    start = [match.start() for match in re.finditer(starts_with, response)]
    # make offer list
    offers = []
    for r in start:
        # link
        end_of_link = response.find('\"',r+9)
        link = response[r+9:end_of_link]
        # name
        start_of_name = end_of_link+17
        end_of_name = response.find('<',start_of_name)
        name = response[start_of_name:end_of_name]
        # description
        start_of_description = response.find('\">',end_of_name) + 2
        end_of_description = response.find('<', start_of_description)
        description = response[start_of_description:end_of_description]
        # year
        start_of_year = response.find('\">',response.find('\">',end_of_description) + 2) + 2
        end_of_year = response.find('<', start_of_year)
        year = response[start_of_year:end_of_year]
        # mileage
        start_of_mileage = response.find('\">',end_of_year) + 2
        end_of_mileage = response.find('<', start_of_mileage)
        mileage = response[start_of_mileage:end_of_mileage]
        # capacity
        start_of_capacity = response.find('\">',end_of_mileage) + 2
        end_of_capacity = response.find('<', start_of_capacity)
        capacity = response[start_of_capacity:end_of_capacity]
        # fuel
        start_of_fuel = response.find('\">', end_of_capacity) + 2
        end_of_fuel = response.find('<', start_of_fuel)
        fuel = response[start_of_fuel:end_of_fuel]
        # city
        end_of_city = response.find("<!", end_of_fuel)
        start_of_city = response.rfind('>', end_of_fuel, end_of_city)
        city = response[start_of_city:end_of_city]
        # province
        start_of_province = response.find('(<!-- -->', end_of_city) + 9
        end_of_province = response.find('<', start_of_province)
        province = response[start_of_province:end_of_province]
        # photo link
        start_of_photo = response.find('https:',end_of_province)
        end_of_photo = response.find('/image',start_of_photo) + 6
        photo = response[start_of_photo:end_of_photo]
        # price
        end_of_price = response.find("PLN", end_of_fuel) + 3
        start_of_price = response.rfind('>', end_of_photo, end_of_price)
        price = response[start_of_price:end_of_price]
        # add to list
        offers.append(Offer(link, name, description, year, capacity, fuel, city, province, photo, price))

    for o in offers:
        print(o.info())
