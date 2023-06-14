import random, discord
from commands.helper import fetchContentList, fetchContent

"""Checks uwuBot's response to see if it is available"""
async def ping(ctx):
    images = fetchContentList('pong.txt')
    num = random.randint(0, len(images)-1)
    embed = discord.Embed(
        title = f'Pong!',
        color = 16251130
    ).set_image(url= images[num])
    embed.set_footer(text='@~ powered by UwUntu')
    
    await ctx.send(embed=embed)

"""Checks uwuBot's response to see if it is available"""
async def pong(ctx):
    images = fetchContentList('pong.txt')
    num = random.randint(0, 22)
    embed = discord.Embed(
        title = f'Ping!',
        color = 16251130
    ).set_image(url= images[num])
    embed.set_footer(text='@~ powered by UwUntu')
    
    await ctx.send(embed=embed)

"""Requests for a link to Anichart to see the in season running anime"""
async def anime(ctx):
    content, f = fetchContent('anichart.txt')
    embed = discord.Embed(
        title = f'Current Anime',
        url = 'https://anilist.co/search/anime/this-season',
        description = content,
        color = 6943230
    ).set_thumbnail(url = 'https://pbs.twimg.com/profile_images/1236103622636834816/5TFL-AFz_400x400.png')
    embed.set_footer(text='@~ powered by UwUntu')

    await ctx.send(embed=embed)
    f.close()

"""Display the list of Authorized Commands to users"""
async def help(ctx):
    commands = fetchContentList('help.txt')

    desc = f'**General Commands**: \n---------------------------------\n'
    for cmd in commands[:len(commands) - 5]:
        desc += f'{cmd}\n'
    
    desc += '\n**Moderator Commands**: \n---------------------------------\n'
    for cmd in commands[len(commands) - 5:]:
        desc += f'{cmd}\n'

    embed = discord.Embed(
        title = f'Help',
        description = desc,
        color = 6943230
    ).set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text='@~ powered by UwUntu')
    
    await ctx.send(embed=embed)