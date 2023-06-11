import discord, block, os
import commands.user as user
import random

from dotenv import load_dotenv
from commands.helper import today, getIcon, getName, todayTime
from commands.manager import pushBlock

load_dotenv()
HUMBLE = int(os.getenv('HUMBLE_ID'))

"""Allow humble to generate free uwu once a day"""
async def humble_powa(ctx, client, BLOCKCHAIN):
    """1. humble can generate uwuCreds based on wng
       2. Usage is checked to function once per day
       3. Blockchain will be validated, new block will be added to end of Blockchain"""
       
    id, name = ctx.author.id, ctx.author.name
    humble_icon = await getIcon(HUMBLE, client)
    """Check if humble has already recieved its daily"""
    if user.hasDaily(HUMBLE, BLOCKCHAIN) == False:
        print('Humble Power: %s - already used Daily' % todayTime())
        return
    
    print('Humble Power: %s - have not used Daily' % todayTime())
    bonus = int(user.getDailyCount(HUMBLE, BLOCKCHAIN) / 7)
    print(bonus)
    
    """Generate new Block"""
    uwu_average, uwu_rng = 600, random.randint(-100, 300)
    submit_rng = random.randint(50, 250)
    total = uwu_average + uwu_rng + submit_rng + bonus*75
    
    new_block = block.Block(
        user = HUMBLE,
        name = 'humble',
        timestamp = today(),
        description = 'Daily',
        data = total
    )
    
    """Update Blockchain"""
    pushBlock(new_block, BLOCKCHAIN)

    desc = f'Beep Boop, I have generated **+{total}** creds, I grow stronger by the moment!\n'
    
    """Return Message"""
    embed = discord.Embed(
        title = 'Daily',
        description = desc,
        color = 16700447    
    ).set_thumbnail(url=humble_icon)
    embed.set_footer(text='@~ powered by UwUntu')
    embed.set_image(url='https://i.ytimg.com/vi/m5KFpQYIYmE/maxresdefault.jpg')

    await ctx.send(embed=embed)

"""Allow humble to either handout his own creds, or take someone else's creds and give it to someone else"""
async def chaos(ctx, client, BLOCKCHAIN):
    """1. Humble randomly determines a set amount
       2. Humble will select 2 users from a list of top 10 candidates that meet the threshold
       3. Humble will either give, take, or move
       4. Blockchain will be validated, new block will be added to end of Blockchain"""
    
    bonus = int(user.getDailyCount(HUMBLE, BLOCKCHAIN) / 7)

    id, name = ctx.author.id, ctx.author.name
    luck = random.random()
    creds = random.randint(100, 200) + 80*bonus

    candidates = user.getTopIds(creds, HUMBLE, BLOCKCHAIN)
    humble_name = await getName(HUMBLE, client)

    userId1, userName1 = candidates[0][0], candidates[0][1] # the hated one
    userId2, userName2 = candidates[1][0], candidates[1][1] # the favored one

    if luck >= 0 and luck < 0.15:
        """Humble gives his own creds to the user"""
        print(f"Humble gives {creds} to {userId2}")

        """Generate new Blocks"""
        new_block1 = block.Block(
            user = HUMBLE,
            name = humble_name,
            timestamp = today(),
            description = f'~Given to {userName2}',
            data = -creds
        )
        new_block2 = block.Block(
            user = userId2,
            name = userName2,
            timestamp = today(),
            description = f'~Recieved from {humble_name}',
            data = creds
        )

        """Update Blockchain"""
        pushBlock(new_block1, BLOCKCHAIN)
        pushBlock(new_block2, BLOCKCHAIN)

        """Return Message"""
        embed = discord.Embed(
            title = f'Humble Love',
            description = f'Humble gave some *love* to <@{userId2}>! (+{creds} uwuCreds)',
            color = 16700447    
        ).set_image(url='https://c.tenor.com/ieCcnZCXV_QAAAAC/tenor.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)

    if luck >= 0.15 and luck < 0.80:
        """Humble takes one random user's creds and gives it to another random user"""
        print(f"Humble moves {creds} from {userId1} to {userId2}")

        """Generate new Blocks"""
        new_block1 = block.Block(
            user = userId1,
            name = userName1,
            timestamp = today(),
            description = f'~Taken by Humble',
            data = -creds
        )
        new_block2 = block.Block(
            user = userId2,
            name = userName2,
            timestamp = today(),
            description = f'~Given by Humble',
            data = creds
        )

        """Update Blockchain"""
        pushBlock(new_block1, BLOCKCHAIN)
        pushBlock(new_block2, BLOCKCHAIN)

        desc = ''
        if userId1 == HUMBLE: desc = f'Humble donated **{creds}** uwuCreds to <@{userId2}>!'
        elif userId2 == HUMBLE: desc = f'Humble charged **{creds}** uwuCreds from <@{userId1}>... for love of course!'
        else: desc = f'Humble lovingly donated **{creds}** uwuCreds to <@{userId2}>! (stolen from <@{userId1}>)'
        
        """Return Message"""
        embed = discord.Embed(
            title = f'Humble Love',
            description = desc,
            color = 16700447    
        ).set_image(url='https://c.tenor.com/JHsVtTnvQ48AAAAC/tenor.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)

    if luck >= 0.80 and luck < 1.0: 
        """Humble takes a random user's creds"""
        print(f"Humble takes {creds} from {userId1}")

        """Generate new Blocks"""
        new_block1 = block.Block(
            user = HUMBLE,
            name = humble_name,
            timestamp = today(),
            description = f'~Taken from {userName1}',
            data = creds
        )
        new_block2 = block.Block(
            user = userId1,
            name = userName1,
            timestamp = today(),
            description = f'~Lost to Humble',
            data = -creds
        )

        """Update Blockchain"""
        pushBlock(new_block1, BLOCKCHAIN)
        pushBlock(new_block2, BLOCKCHAIN)

        """Return Message"""
        embed = discord.Embed(
            title = f'Humble Love',
            description = f'Humble took **{creds}** uwuCreds from <@{userId1}>!',
            color = 16700447    
        ).set_image(url='https://pa1.narvii.com/6306/e69ecf1e4912220c77f1dd9b0e710dedb26639b0_hq.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed) 