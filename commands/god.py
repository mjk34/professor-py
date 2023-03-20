import discord, block, blockchain, random, os

from dotenv import load_dotenv
from commands.helper import today, getName
from commands.stats import stats, getStat, disabledUpgrade

load_dotenv()
ADMIN = int(os.getenv('ADMIN_ID'))

# async def return_to_the_stars(ctx, client, BLOCKCHAIN):
#     user_id, name = ctx.author.id, ctx.author.name
#     if user_id != ADMIN:
#        embed = discord.Embed(
#             title = f'Return To The Stars',
#             description = f'Insufficient power, you are not *god*!',
#             color = 6053215    
#         ).set_thumbnail(url='https://c.tenor.com/hal0bUXw_mYAAAAC/giyuu-tomioka-demon-slayer.gif')
#        embed.set_footer(text='@~ powered by UwUntu')
#        await ctx.send(embed=embed)
#        return
    
#     # get all unique ids
#     unique_ids = []
#     for i in BLOCKCHAIN.chain[1:]:
#         unique_ids.append(i.getUser())
#     unique_ids = list(set(unique_ids))

#     # run through each user, and check each stat
#     # get a count of each stat level, add count to user_stars
#     # create counter stat so each stat sits at level 0
#     for id in unique_ids:
#         id_name = await getName(id, client)
#         user_stars = 0
#         for stat in stats:
#             level = getStat(id, stat, BLOCKCHAIN)
#             user_stars += level

#             counter_stat = '-' + stat
#             for i in range(level):
#                 new_block = block.Block(
#                     user = id,
#                     name = id_name,
#                     timestamp = today(),
#                     description = counter_stat,
#                     data = 0
#                 )

#                 """Update Blockchain"""
#                 if BLOCKCHAIN.isChainValid() == False:
#                     print('The current Blockchain is not valid, performing rollback.')
#                     BLOCKCHAIN = blockchain.Blockchain()

#                 BLOCKCHAIN.addBlock(new_block)
#                 if BLOCKCHAIN.isChainValid():
#                     BLOCKCHAIN.storeChain()
                
#         for i in range(user_stars):
#             star_block = block.Block(
#                 user = id,
#                 name = id_name,
#                 timestamp = today(),
#                 description = 'Star',
#                 data = 0
#             )

#             """Update Blockchain"""
#             if BLOCKCHAIN.isChainValid() == False:
#                 print('The current Blockchain is not valid, performing rollback.')
#                 BLOCKCHAIN = blockchain.Blockchain()

#             BLOCKCHAIN.addBlock(star_block)
#             if BLOCKCHAIN.isChainValid():
#                 BLOCKCHAIN.storeChain() 

#     """Return Message"""
#     embed = discord.Embed(
#         title = f'Return to The Stars',
#         description = "Operation Success",
#         color = 2352682,
#     ).set_thumbnail(url=ctx.author.avatar_url)
#     embed.set_footer(text='@~ powered by UwUntu')
#     await ctx.send(embed=embed)
#     return

# async def disable_upgrade(ctx, BLOCKCHAIN):
#     id, name = ctx.author.id, ctx.author.name
#     if id != ADMIN:
#        embed = discord.Embed(
#             title = f'Return To The Stars',
#             description = f'Insufficient power, you are not *god*!',
#             color = 6053215    
#         ).set_thumbnail(url='https://c.tenor.com/hal0bUXw_mYAAAAC/giyuu-tomioka-demon-slayer.gif')
#        embed.set_footer(text='@~ powered by UwUntu')
#        await ctx.send(embed=embed)
#        return
    
#     disable_block = block.Block(
#         user = 69,
#         name = 'SYSTEM',
#         timestamp = today(),
#         description = 'Disable Upgrade',
#         data = 0
#     )

#     """Update Blockchain"""
#     if BLOCKCHAIN.isChainValid() == False:
#         print('The current Blockchain is not valid, performing rollback.')
#         BLOCKCHAIN = blockchain.Blockchain()
    
#     BLOCKCHAIN.addBlock(disable_block)
#     if BLOCKCHAIN.isChainValid():
#         BLOCKCHAIN.storeChain()

#     desc, color = '', 0
#     if disabledUpgrade(BLOCKCHAIN):
#         desc = '/Upgrade has been disabled'
#         color = 6053215
#     else: 
#         desc = '/Upgrade has been enabled'
#         color = 2352682

#     """Return Message"""
#     embed = discord.Embed(
#         title = f'Disable Upgrade',
#         description = desc,
#         color = color,
#     ).set_thumbnail(url=ctx.author.avatar_url)
#     embed.set_footer(text='@~ powered by UwUntu')
#     await ctx.send(embed=embed)
#     return

async def hand_all(ctx, amount, client, BLOCKCHAIN) -> list:
    id, name = ctx.author.id, ctx.author.name
    if id != ADMIN:
       embed = discord.Embed(
            title = f'Hand All',
            description = f'Insufficient power, you are not *god*!',
            color = 6053215    
        ).set_thumbnail(url='https://c.tenor.com/hal0bUXw_mYAAAAC/giyuu-tomioka-demon-slayer.gif')
       embed.set_footer(text='@~ powered by UwUntu')
       await ctx.send(embed=embed)
       return
    
    unique_ids = []
    for i in BLOCKCHAIN.chain[1:]:
        unique_ids.append(i.getUser())
    unique_ids = list(set(unique_ids))
    
    for id in unique_ids:
        id_name = await getName(id, client)
        new_block = block.Block(
            user = id,
            name = id_name,
            timestamp = today(),
            description = 'Handout',
            data = amount
        )

        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
        
        BLOCKCHAIN.addBlock(new_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()
    
    desc = f'Absolute Decree! **{amount}** uwuCreds has been ordained to all users.'

    """Return Message"""
    embed = discord.Embed(
        title = f'Hand All',
        description = desc,
        color = 2352682,
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
    return

async def take_level (ctx, reciever, stat_name, client, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name
    if id != ADMIN:
       embed = discord.Embed(
            title = f'Hand All',
            description = f'Insufficient power, you are not *god*!',
            color = 6053215    
        ).set_thumbnail(url='https://c.tenor.com/hal0bUXw_mYAAAAC/giyuu-tomioka-demon-slayer.gif')
       embed.set_footer(text='@~ powered by UwUntu')
       await ctx.send(embed=embed)
       return
    
    """Parses Reciever id from <@id>"""
    reciever_id = reciever
    filler = ['<', '>', '!', '@', '&']

    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

    counter_stat = ''
    if stat_name.lower() == 'vitality' or stat_name.lower() == 'vit':
        counter_stat = '-Vitality'
    if stat_name.lower() == 'stamina' or stat_name.lower() == 'sta':
        counter_stat = '-Stamina'
    if stat_name.lower() == 'strength' or stat_name.lower() == 'str':
        counter_stat = '-Strength'
    if stat_name.lower() == 'dexterity' or stat_name.lower() == 'dex':
        counter_stat = '-Dexterity'
    if stat_name.lower() == 'ego':
        counter_stat = '-Ego'
    if stat_name.lower() == 'fortune' or stat_name.lower() == 'for':
        counter_stat = '-Fortune'

    reciever_name = await getName(reciever_id, client)
    new_block = block.Block(
        user = reciever_id,
        name = reciever_name,
        timestamp = today(),
        description = counter_stat,
        data = 0
    )

    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
    
    BLOCKCHAIN.addBlock(new_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()

    desc = f'A level of {counter_stat[1:]} was taken from <@{reciever_id}>'

    """Return Message"""
    embed = discord.Embed(
        title = f'Take Level',
        description = desc,
        color = 2352682,
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
    return