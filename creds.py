import discord, block, blockchain

from dotenv import load_dotenv
from discord.utils import get

#from helper1 import dailyLuck, getTime, lessThan24HRs, timeWait, timeDiff
#from helper1 import rewardCost
from helper import today, dailyLuck

filler = ['<', '>', '!', '@']

async def dailyUwU (ctx, BLOCKCHAIN):
    """1. Users can generate uwuCreds based on rng
       2. Usage is checked to function once per day
       3. Blockchain will be validated, new block will be added to end of blockchain"""
    id, name = ctx.author.id, ctx.author.name

    # """check if the user has used the command less than 20hrs ago"""
    # user_daily = api.fetchDaily(id)
    # time_diff = timeDiff(user_daily, today)
    # if lessThan24HRs(time_diff):
    #     await ctx.send(f'<@{id}>, your next **/uwu** resets in **{timeWait(time_diff)}**')
    #     return
    
    """Generate new Block"""
    fortune, status = dailyLuck()
    new_block = block.Block(
        user = id,
        timestamp = today(),
        description = 'Daily',
        data = fortune
    )
    
    """Update Blockchain"""
    if not BLOCKCHAIN.isChainValid():
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(new_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()           
    BLOCKCHAIN.printChain()
    
    embed = discord.Embed(
        title = f'Daily UwU',
        description = f'{status} **+{fortune}** creds were added to your *Wallet*!',
        color = 16700447    
    ).set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)