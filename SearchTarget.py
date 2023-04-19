import time
import requests
import html
import re
from Offer import Offer
from otomotoAPI import extractOffersFromResponse, findNewOffers


class SearchTarget:
    def __init__(self, search_url, channel_id, user_id, add_date):
        self.search_url = search_url
        self.channel_id = channel_id
        self.user_id = user_id
        self.add_date = add_date
        self.last_offer = [None]

    def checkForNewOffers(self):
        response = requests.get(self.search_url)
        response_raw = html.unescape(response.text);
        # print(response.text)
        # with open("response.txt", "wb") as file:
        #    file.write(response.content)

        # s1 = time.time()
        offers = extractOffersFromResponse(response_raw)
        # print(f' @ extractOffersFromResponse took: {time.time() - s1:.3f}s')
        # s2 = time.time()
        return findNewOffers(offers, self.last_offer)
        # print(f' @ findNewOffers took: {time.time() - s2:.3f}s')





