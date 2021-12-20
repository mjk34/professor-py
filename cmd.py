import random
import discord

async def pong(ctx):
    num = random.randint(1, 23)
    filename = f'./pong/{num}.jpg'
    f = open(filename, 'rb')
    await ctx.send('Pong!', file=discord.File(f))
    f.close()

async def halp(ctx):
    author = ctx.author
    content, f = fetchContent(ctx.name, True)
    await author.send(content)
    await ctx.send('Sent ya the detes, check your dm.')
    f.close()

async def playlist(ctx):
    message_size = 2000
    f = fetchContent(ctx.name, False)

    while True:
        message_chunk = f.read(message_size)
        if message_chunk == '': break
        await ctx.send(message_chunk)  
    f.close()

async def fetchMSG (ctx):
    content, f = fetchContent(ctx.name, True)
    await ctx.send(content)
    f.close()

def fetchContent (filename, read):
    filename = f'./messages/{filename}.txt'
    f = open(filename, 'r')
    if read: return f.read(), f
    else: return f