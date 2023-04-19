# bot.py
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
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
client = discord.Client(intents=discord.Intents.all())

searches = []

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )
    test.start()

@tasks.loop(seconds=20)
async def test():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(datetime.now().strftime(" @: %H:%M.%S"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '$channelid':
        response = 'channelID: \"' + str(message.channel.id) + '\"'
        await message.channel.send(response)
    if message.content.lower() == '$test':
        await message.channel.send('starting...')
        s1 = time.time()
        otomotoAPI.test()
        await message.channel.send(f'...done [took: {time.time()-s1:.2f}s]')
    if message.content.lower().startswith('$search'):
        user_id = message.author
        channel_id = message.channel.id
        search_url = message.content[len('$search'):].strip()
        searches.append(SearchTarget(search_url, channel_id, user_id, datetime.now()))
        await message.channel.send(f'ok {user_id.mention} i added search for your url (<{search_url}>)')
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
            del searches[index]
            await message.channel.send(embed=embed)

client.run(TOKEN)