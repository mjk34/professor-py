import random
import discord

async def pong(message):
    num = random.randint(1, 23)

    filename = f'./pong/{num}.jpg'
    f = open(filename, 'rb')

    await message.channel.send('Pong!', file=discord.File(f))
    f.close()

async def halp(message):
    author = message.author

    filename = f'./messages/help.txt'
    f = open(filename, 'r')
    help_message = f.read()

    await author.send(help_message)
    f.close()

async def playlist(message):
    message_size = 2000
    filename = f'./messages/music.txt'
    f = open(filename, 'r')

    while True:
        message_chunk = f.read(message_size)
        if message_chunk == '': break

        await message.channel.send(message_chunk)  
    f.close()

async def mal (message):
    filename = f'./messages/mal.txt'
    f = open(filename, 'r')
    message_txt = f.read()

    await message.channel.send(message_txt)
    f.close()

async def anichart (message):
    filename = f'./messages/aniChart.txt'
    f = open(filename, 'r')
    message_txt = f.read()

    await message.channel.send(message_txt)
    f.close()