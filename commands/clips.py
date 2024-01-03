import discord, block

from commands.manager import pushBlock
from commands.helper import today

filler = ['<', '>', '!', '@']
        
clip_source = ['https://medal.tv/games', 'https://www.youtube.com/']
        
"""Allow users to submit a Valorant game to earn uwuCreds"""
async def submitClip(ctx, title, link, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user submissions will be checked
       2. Blockchain will be validated, new block will be added to the end of Blockchain"""
    
    id, name = ctx.author.id, ctx.author.name
    color = 6053215
    
    """check if the link is actually a clip link relating to medal or youtube"""
    if clip_source[0] not in link and clip_source[1] not in link:
        embed = discord.Embed(
            title = f'Submission',
            description = f'Link Error: Supported platforms for clips are youtube and medal.tv (non-clip submits have been discontinued)',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    color = 6943230
            
    """Generate new Block"""
    submit_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Submission',
        data = 200
    )

    """Update Blockchain"""
    pushBlock(submit_block, BLOCKCHAIN)
            
    """Return Message"""
    desc = f'Title: \u3000**{title}**\n'
    desc += f'Link: \u3000**{link}**\n'

    desc2 = f'Thank you for submitting, **{200}** creds were added to your *Wallet*!\n'

    embed = discord.Embed(
        title = f'Submission',
        description = desc,
        color = color    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
    await ctx.send(desc2)