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
        link = response[r+9:response.find('\"',r+9)]
        offers.append(Offer(link))
    #print(offers)
    print([offer.link for offer in offers])
