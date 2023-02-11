import discord, block, blockchain
import commands.user as user

from discord.utils import get
from commands.helper import getName
from commands.stats import getStamina, getStrength, getDexterity
from commands.helper import today

filler = ['<', '>', '!', '@']
        
"""Allow users to submit a Valorant game to earn uwuCreds"""
async def submitClip(ctx, title, link, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user submissions will be checked
       2. Blockchain will be validated, new block will be added to the end of Blockchain"""
    id, name = ctx.author.id, ctx.author.name
    stamina = getStamina(id, BLOCKCHAIN) 
    strength = getStrength(id, BLOCKCHAIN)

    color = 6053215

    """check if the user has submissions left"""
    user_subs = user.totalSubsWeek(id, BLOCKCHAIN)
    if user_subs >= (5 + stamina):
        embed = discord.Embed(
            title = f'Submission',
            description = f'Out of Submissions, Submissions will reset every Monday!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    color = 6943230
            
    """Generate new Block"""
    new_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = 'Submission',
        data = 200 + 40*strength
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
    desc = f'Title: \u3000**{title}**\n'
    desc += f'Link: \u3000**{link}**\n'
    desc2 = f'Thank you for submitting, **{200}** creds were added to your *Wallet*! If you submitted a clip, check the events tab to see when is the next Clip Night!\n'
    
    if strength > 0:
        desc2 += f'\nFrom **Strength {strength}**, you get an additional **+{int(40*strength)}** creds!'
    embed = discord.Embed(
        title = f'Submission',
        description = desc,
        color = color    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    message_to_pin = await ctx.send(embed=embed)

    await ctx.send(desc2)
    
    if link == 'NA' or link == 'N/A' or link == 'na': return
    await message_to_pin.pin()

async def review(ctx, reciever, rating, client, BLOCKCHAIN):
    """1. User will be checked for Moderator status
       2. Blockchain will be validated, new blocks will be added to the end of Blockchain"""
    
    """Parses Reciever id from <@id>"""
    reciever_id = reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

    dexterity = getDexterity(reciever_id, BLOCKCHAIN)
    dex_bonus = int((40*rating)*(0.25*dexterity))

    """Check if the Giver is a moderator"""
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        
        """Generate new Block"""
        new_block = block.Block(
            user = reciever_id,
            name = await getName(reciever_id, client),
            timestamp = today(),
            description = f'Review from {ctx.author.name}',
            data = 40*rating + dex_bonus
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
    
        BLOCKCHAIN.addBlock(new_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           
        
        desc = f'<@{reciever_id}> recieved {rating} Rating for this Clip Night! **{40*rating}** was rewarded.\n\n'
        if dexterity > 0:
            desc += f'From **Dexterity {dexterity}**, you get an additional **+{dex_bonus}** creds!'

        """Return Message"""
        embed = discord.Embed(
            title = f'Clip Review',
            description = desc,
            color = 16749300    
        ).set_image(url='https://3.bp.blogspot.com/-SmBYkUqPhOE/Vjq6UpF5StI/AAAAAAAAYsI/b1iXLlfx3ys/s640/food%2Bwars%2B1.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
    else: 
        embed = discord.Embed(
            title = f'Handout',
            description = f'Insufficient power, you are not a moderator!',
            color = 6053215    
        ).set_thumbnail(url='https://media1.tenor.com/images/80662c4e35cf12354f65f1d6f7beada8/tenor.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
    return