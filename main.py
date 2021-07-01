import os

import discord
from dotenv import load_dotenv

import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

START_CMD_WITH = '>'

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author.guild.name != GUILD:
        return
    if message.author == client.user:
        return

    # Check if first character does bot stuff
    message_string = message.content.lower()
    if message_string[0] != START_CMD_WITH:
        return

    # Get the rest of the message
    message_string = message_string[1:]

    if 'ping' in message_string:
        num = random.randint(1, 23)
        filename = f'./pong/{num}.jpg'
        f = open(filename, 'rb')
        await message.channel.send('Pong!', file=discord.File(f))
        f.close()
client.run(TOKEN)

