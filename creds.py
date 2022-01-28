import discord, block, blockchain
import user

from dotenv import load_dotenv
from discord.utils import get

#from helper1 import dailyLuck, getTime, lessThan24HRs, timeWait, timeDiff
#from helper1 import rewardCost
from helper import today, dailyLuck, dailyFortune

filler = ['<', '>', '!', '@']

async def daily (ctx, BLOCKCHAIN):
    """1. Users can generate uwuCreds based on rng
       2. Usage is checked to function once per day
       3. Blockchain will be validated, new block will be added to end of blockchain"""
       
    id = ctx.author.id
    if user.hasDaily(id, BLOCKCHAIN) == False:
        embed = discord.Embed(
            title = f'Daily',
            description = f'You next **/uwu** is tomorrow, it now resets based on date!',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by oogway desu')
        
        await ctx.send(embed=embed)
        return
    
    """Generate new Block"""
    fortune, status = dailyLuck()
    new_block = block.Block(
        user = id,
        timestamp = today(),
        description = 'Daily',
        data = fortune
    )
    
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(new_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()           
    #BLOCKCHAIN.printChain()
    
    embed = discord.Embed(
        title = f'Daily',
        description = f'{status} **+{fortune}** creds were added to your *Wallet*!',
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by oogway desu')
    embed.add_field(
        name = 'Fortune',
        value = dailyFortune()
    )
    await ctx.send(embed=embed)