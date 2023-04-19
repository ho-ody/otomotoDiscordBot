# bot.py
from datetime import datetime
import os
import time

import discord
from discord.ext import tasks
from dotenv import load_dotenv

import otomotoAPI

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
client = discord.Client(intents=discord.Intents.all())

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

client.run(TOKEN)