import discord, block, blockchain
import commands.user as user
import math

from commands.helper import today, getWeight

filler = ['<', '>', '!', '@']
        
"""Allow users to submit a Valorant game to earn uwuCreds"""
async def getOWScore(ctx, title, link, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user submissions will be checked
       2. Blockchain will be validated, new block will be added to the end of Blockchain"""
    id, name = ctx.author.id, ctx.author.name
    color = 6053215

    """check if the user has submissions left"""
    user_subs = user.totalSubsWeek(id, 'O', BLOCKCHAIN)
    if user_subs >= 10:
        embed = discord.Embed(
            title = f'Submission',
            description = f'Out of Overwatch Submissions, it now resets every Monday!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    color = 15814693
            
    """Generate new Block"""
    new_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Submission O',
        data = 100
    )

    clip_block = block.Block(
        user = 69,
        name = "Clip",
        timestamp = today(),
        description = f'{title}^{link}',
        data = 0
    )
            
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
        
    BLOCKCHAIN.addBlock(new_block)
    BLOCKCHAIN.addBlock(clip_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()           
            
    """Return Message"""
    desc = 'Overwatch Game:\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\n\n'
    desc += f'Title: \u3000**{title}**\n'
    desc += f'Link: \u3000**{link}**\n\n'
    desc += f'Thank you for submitting, **100** creds were added to your *Wallet*! If you submitted a clip, they will be reviewed at a later date!'
    embed = discord.Embed(
        title = f'Submission',
        description = desc,
        color = color    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    message_to_pin = await ctx.send(embed=embed)   
    
    if link == 'NA' or link == 'N/A' or link == 'na': return
    await message_to_pin.pin()