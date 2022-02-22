import discord, block, blockchain, os
from pyrsistent import b
import commands.user as user
import random

from dotenv import load_dotenv
from commands.helper import today

load_dotenv()
HUMBLE = int(os.getenv('HUMBLE_ID'))

"""Allow humble to generate free uwu once a day"""
async def humble_powa(ctx, BLOCKCHAIN):
    """1. humble can generate uwuCreds based on wng
       2. Usage is checked to function once per day
       3. Blockchain will be validated, new block will be added to end of Blockchain"""
       
    id, name = ctx.author.id, ctx.author.name
    """Check if humble has already recieved its daily"""
    if user.hasDaily(HUMBLE, BLOCKCHAIN) == False:
        embed = discord.Embed(
            title = f'Daily',
            description = f'My Creator says I\'m fat, I shall fast until tomorrow!',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by oogway desu')
        embed.set_image(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2FK6SZyj7A3AU%2Fmaxresdefault.jpg')
        await ctx.send(embed=embed)
        return
    
    bonus = int(user.getDailyCount(HUMBLE, BLOCKCHAIN) / 10)
    print(bonus)
    
    """Generate new Block"""
    uwu_average, uwu_rng = 420, random.randint(-50, 50)
    total = uwu_average + uwu_rng + bonus*60
    
    val_average = 300
    for i in range(3):
        val_rng = random.randint(-50, 50)
        total += val_average + val_rng
    
    total += 100 + bonus*60
    
    new_block = block.Block(
        user = HUMBLE,
        name = 'humble',
        timestamp = today(),
        description = 'Daily',
        data = total
    )
    
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(new_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()           
    BLOCKCHAIN.printChain()

    desc = f'Beep Boop, I have generated **+{total}** creds, I grow stronger by the moment!\n'
    
    """Return Message"""
    embed = discord.Embed(
        title = 'Daily',
        description = desc,
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by oogway desu')
    embed.set_image(url='https://i.ytimg.com/vi/m5KFpQYIYmE/maxresdefault.jpg')

    await ctx.send(embed=embed)