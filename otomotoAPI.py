import time

import discord
import requests
import html
import re

from Offer import Offer


# last_offer = None

async def test():
    testurl1 = 'https://www.otomoto.pl/osobowe/audi/a3/rzeszow?search%5Bfilter_enum_fuel_type%5D=diesel&search%5Bdist%5D=200&search%5Bfilter_float_mileage%3Ato%5D=200000&search%5Bfilter_float_price%3Afrom%5D=15000&search%5Bfilter_float_price%3Ato%5D=20000&search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true'
    testurl2 = 'https://www.otomoto.pl/osobowe/audi/a3?search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true'
    testurl3 = 'https://www.otomoto.pl/osobowe/audi?search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true'
    testurl4 = 'https://www.otomoto.pl/osobowe/citroen?search%5Border%5D=created_at_first%3Adesc'
    # This will yield only the HTML code
    url = testurl1
    url = testurl2
    url = testurl3
    # url = testurl4
    response = requests.get(url)
    response_raw = html.unescape(response.text);
    # print(response.text)
    with open("response.txt", "wb") as file:
        file.write(response.content)

    s1 = time.time()
    offers = extractOffersFromResponse(response_raw)
    print(f' @ extractOffersFromResponse took: {time.time() - s1:.3f}s')
    s2 = time.time()
    await findNewOffers(offers)
    print(f' @ findNewOffers took: {time.time() - s2:.3f}s')

def extractOffersFromResponse(response: str):
    starts_with = '<a href="https://www.otomoto.pl/oferta/'
    # find all text occurrences
    start = [match.start() for match in re.finditer(starts_with, response)]
    # make offer list
    offers = []
    for i, r in enumerate(start):
        # link
        end_of_link = response.find('\"', r + 9)
        link = response[r + 9:end_of_link]
        # name
        start_of_name = end_of_link + 17
        end_of_name = response.find('<', start_of_name)
        name = response[start_of_name:end_of_name]
        # description
        if i == 0:  # different formatting in first one
            start_of_description = response.rfind('\">', end_of_name, response.find('</p>', end_of_name)) + 2
        else:
            while response.find('@media',end_of_name) < response.find('\">', end_of_name):
                end_of_name = response.find('\">',end_of_name) + 2
            start_of_description = response.find('\">', end_of_name) + 2
        end_of_description = response.find('<', start_of_description)
        description = response[start_of_description:end_of_description]
        if description != "":   # different formatting when no description
            end_of_description = response.find('\">', end_of_description) + 2
        # year
        if i == 0:  # different formatting in first one
            start_of_year = response.find('\">', response.find('\">', response.find('ul class', response.find('ul class', end_of_description) + 2)) + 2) + 2
        elif response.find('</p><style', response.find('<', start_of_description)) < response.find('\">', response.find('<', start_of_description) + 2):  # need new otomoto format fix
            # end_of_description = response.find('ul class', end_of_description) + 2
            start_of_year = response.find('\">', response.find('\">', response.find('ul class', response.find('<', start_of_description)) + 2) + 2) + 2
        else:
            start_of_year = response.find('\">', end_of_description) + 2
        end_of_year = response.find('<', start_of_year)
        year = response[start_of_year:end_of_year]
        # mileage
        start_of_mileage = response.find('\">', end_of_year) + 2
        end_of_mileage = response.find('<', start_of_mileage)
        mileage = response[start_of_mileage:end_of_mileage]
        # capacity
        if mileage.find('km') == -1:    # no mileage given for some reason
            start_of_capacity = start_of_mileage
            end_of_capacity = end_of_mileage
            mileage = '0 km'
        else:
            start_of_capacity = response.find('\">', end_of_mileage) + 2
            end_of_capacity = response.find('<', start_of_capacity)
        capacity = response[start_of_capacity:end_of_capacity]
        # fuel
        start_of_fuel = response.find('\">', end_of_capacity) + 2
        end_of_fuel = response.find('<', start_of_fuel)
        fuel = response[start_of_fuel:end_of_fuel]
        # city
        end_of_city = response.find("<!", end_of_fuel)
        start_of_city = response.rfind('>', end_of_fuel, end_of_city) + 1
        city = response[start_of_city:end_of_city]
        # province
        start_of_province = response.find('(<!-- -->', end_of_city) + 9
        end_of_province = response.find('<', start_of_province)
        province = response[start_of_province:end_of_province]
        # publication date
        start_of_date = response.find('\">', end_of_province) + 2
        end_of_date = end_of_province = response.find('<', start_of_date)
        date = response[start_of_date:end_of_date]
        # photo link
        start_of_photo = response.find('src=\"https:', end_of_province) + 5
        end_of_photo = response.find('/image', start_of_photo) + 6
        photo = response[start_of_photo:end_of_photo]
        # price
        end_of_price = response.find("PLN", end_of_fuel) + 3
        start_of_price = response.rfind('>', end_of_date, end_of_price) + 1
        price = response[start_of_price:end_of_price]
        # add to list
        offers.append(Offer(link, name, description, year, mileage, capacity, fuel, city, province, date, photo, price))

    #for o in offers:
    #    print(o.info())
    return offers

async def findNewOffers(offers, last_offer, printNewOffers, searchTarget):
    """
    :type offers: Offer[]
    """
    new_offers = []
    for o in offers:
        if last_offer[0] and o == last_offer[0]:
            break
        if not checkIfDateShouldBeCount(o.date):
            break
        new_offers.append(o)

    if len(offers):
        last_offer[0] = offers[0]
    else:
        last_offer[0] = None

    if printNewOffers:
        for o in new_offers:
            print(o.info())
            await sendMessage(searchTarget, o)
    return len(new_offers)

def checkIfDateShouldBeCount(date: str):
    date = date[len('Opublikowano '):]
    if not date.find('minut') != -1:
        return False
    minutes = date[:date.find(' ')]
    minutes = int(minutes)
    if minutes > 20:
        return False
    return True


def embedOffer(offer: Offer):
    embed = discord.Embed(title=offer.name, description=offer.description, color=0x00ff4c)
    embed.set_image(url=offer.photo)
    embed.add_field(name='price', value=offer.price, inline=True)
    embed.add_field(name='mileage', value=offer.mileage, inline=True)
    embed.add_field(name='year', value=offer.year, inline=True)
    embed.add_field(name='engine', value=offer.capacity+'  '+offer.fuel, inline=True)
    embed.add_field(name='city', value=offer.city + '  (' + offer.province + ')', inline=True)
    embed.add_field(name='', value='', inline=True)
    embed.add_field(name='link', value=offer.link, inline=False)
    return embed

async def sendMessage(searchTarget, offer: Offer):
    channel = searchTarget.channel_id
    await channel.send(f'{searchTarget.user_id.mention}', embed=embedOffer(offer))

