import random
import discord
import requests

async def pong(message):
    num = random.randint(1, 23)
    filename = f'./pong/{num}.jpg'
    f = open(filename, 'rb')

    await message.channel.send('Pong!', file=discord.File(f))
    f.close()

async def halp(message, command):
    author = message.author
    fetchMessage(command)
    content, f = fetchTemp(True)

    await author.send(content)
    f.close()

async def playlist(message, command):
    message_size = 2000
    fetchMessage(command)
    f = fetchTemp(False)

    while True:
        message_chunk = f.read(message_size)
        if message_chunk == '': break

        await message.channel.send(message_chunk)  
    f.close()

async def fetchMSG (message, command):
    fetchMessage(command)
    content, f = fetchTemp(True)

    await message.channel.send(content)
    f.close()

def fetchMessage (filename):
    print('\n' + filename + '\n')
    url = f'https://raw.githubusercontent.com/Mkadzis23/uwuBot/main/messages/{filename}.txt'
    page = requests.get(url)
    content = page.text
    
    filename = f'./messages/temp.txt'
    with open(filename, 'w') as temp:
        temp.write(content)

def fetchTemp (read):
    filename = f'./messages/temp.txt'
    f = open(filename, 'r')

    if read: return f.read(), f
    else: return f