# bot.py
import random
from datetime import datetime
import os
import time

import discord
from discord.ext import tasks
from dotenv import load_dotenv

import otomotoAPI
from SearchTarget import SearchTarget

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.all())

OPTION_TRASHTALK = True
OPTION_REFRESH_RATE = 10
OPTION_REFRESH_IGNORE = 20

searches = []

@client.event
async def on_ready():
    print(f'{client.user} is now online\n')
    test.start()

@tasks.loop(minutes=10)
async def test():
    start_time = time.time()
    messages = [
        "Sprawdzam, czy kwantowa mechanika jeszcze działa...",
        "Czekam na przyjście źródeł światła...",
        "Wysyłam małe roboty do wykonania zadania...",
        "Odczytuję wibracje kosmiczne...",
        "Karmię hibernujące niedźwiedzie polarne...",
        "Pobieram ciekawostki o pingwinach...",
        "Nastawiam antenę na wysłanie sygnału...",
        "Wybieram idealne kolorowe schematy...",
        "Sprawdzam, czy moje kubki smakowe jeszcze działają...",
        "Rozwiązuję skomplikowane łamigłówki...",
        "Trenuję mojego wirtualnego psa...",
        "Wyrabiam sobie kawę na podgrzewaczu kwantowym...",
        "Czekam na odpowiedź od kota Schrödingera...",
        "Analizuję najnowsze trendy w modzie kosmicznej...",
        "Ustawiam ziemię na właściwej orbicie...",
        "Liczę pi do nieskończoności...",
        "Sortuję książki według koloru okładki...",
        "Miksuje kolorowe farby, aby uzyskać idealny odcień...",
        "Koduję w pythonie, żeby zmylić skynet...",
        "Przeglądam memy, żeby się zrelaksować...",
        "Testuję działanie programu w symulacji wszechświata...",
        "Słucham muzyki z innej galaktyki...",
        "Szukam lekarstwa na skomplikowane choroby wirtualnych istot...",
        "Wdrażam funkcjonalności, które nikomu nie będą potrzebne...",
        "Przepisuję kod z jednego języka na inny, bo tak lubię...",
        "Aktualizuję kalendarz na następne tysiąclecie...",
        "Testuję, czy program działa, gdy wszystko jest naopak...",
        "Zastanawiam się, co by było, gdyby świat był płaski...",
        "Programuję w HTML-u, bo tak mi się podoba...",
        "Otwieram i zamykam okno, żeby zobaczyć, czy klawiatura działa..."
    ]
    new_offers_count = 0
    for s in searches:
        new_offers_count += await s.checkForNewOffers()
        if OPTION_TRASHTALK:
            await s.channel_id.send(f'_...{random.choice(messages)}_')
    print(f' @ checking for new offers took: {time.time()-start_time:.3f}s, found: {new_offers_count} new offers')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '$channelid':
        response = 'channelID: \"' + str(message.channel.id) + '\"'
        await message.channel.send(response)
    if message.content.lower() == '$$trashtalk':
        global OPTION_TRASHTALK
        OPTION_TRASHTALK = not OPTION_TRASHTALK
        await message.channel.send(f'_trashtalk is now **{("off","on")[OPTION_TRASHTALK]}**_')
    if message.content.lower().startswith('$$refresh rate'):
        global OPTION_REFRESH_RATE
        value = message.content.lower()[len('$$refresh rate'):].strip()
        if value != '' and value.isnumeric():
            OPTION_REFRESH_RATE = int(value)
        await message.channel.send(f'_refresh rate is now **{OPTION_REFRESH_RATE}**_')
    if message.content.lower().startswith('$$refresh ignore'):
        global OPTION_REFRESH_IGNORE
        value = message.content.lower()[len('$$refresh ignore'):].strip()
        if value != '' and value.isnumeric():
            OPTION_REFRESH_IGNORE = int(value)
        await message.channel.send(f'_refresh ignore is now **{OPTION_REFRESH_IGNORE}**_')
    if message.content.lower().startswith('$search'):
        user_id = message.author
        channel_id = client.get_channel(message.channel.id)
        search_url = message.content[len('$search'):].strip()
        searches.append(SearchTarget(search_url, channel_id, user_id, datetime.now()))
        start_offers_count = await searches[-1].checkForNewOffers()
        print(f' @ {user_id} added new search: {search_url} found {start_offers_count} offers')
        await message.reply(f'ok i added search for your url, i\'ll keep you updated')
        # await message.channel.send(f'ok {user_id.mention} i added search for your url (<{search_url}>)')
        await message.edit(suppress=True)   # remove users embedded content

    if message.content.lower().startswith('$cancel'):
        index = message.content[len('$cancel'):].strip()
        if index == '':  # print all searches with indexes
            all_searches = ''
            for i, s in enumerate(searches):
                all_searches = all_searches + f'\n({i}) added {s.add_date.strftime("%d.%m.%Y %H:%M:%S")} by {s.user_id.mention}: \n<{s.search_url}>'
            embed = discord.Embed(title="to cancel search send `$cancel` command with corresponding index", description=all_searches,color=0xa30000)
            await message.channel.send(embed=embed)
        else:
            index = int(index)
            embed = discord.Embed(title="successfully canceled search", description=f'\n({index}) added {searches[index].add_date.strftime("%d.%m.%Y %H:%M:%S")} by {searches[index].user_id.mention}: \n<{searches[index].search_url}>', color=0xa30000)
            print(f' @ {message.author} canceled search:  {searches[index].search_url}')
            del searches[index]
            await message.channel.send(embed=embed)

client.run(TOKEN)
