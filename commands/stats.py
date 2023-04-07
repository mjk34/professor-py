import discord, block, blockchain, random, os
import commands.user as user

from dotenv import load_dotenv
from commands.helper import today, getName

filler = ['<', '>', '!', '@', '&']
stats = [
    "Vitality",     #0
    'Stamina',      #1
    'Strength',     #2
    'Dexterity',    #3 
    'Ego',          #4
    'Fortune',      #5
]

load_dotenv()
HUMBLE = int(os.getenv('HUMBLE_ID'))
ADMIN = int(os.getenv('ADMIN_ID'))
HBOT = 904417820899700756

"""Allow users to view their stat progress and benefits"""
"""Vitality, Stamina, Strength, Dexterity, Fortune, Star"""

async def profile (ctx, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name

    star = getStar(id, BLOCKCHAIN)
    reforger = getReforger(id, BLOCKCHAIN)
    dark_star = getDarkStar(id, BLOCKCHAIN)

    vitality = getStat(id, stats[0], BLOCKCHAIN)
    vit_scale = int(0.1*vitality - pow(vitality, (0.008*vitality)) + 1)

    vit_str = f' **+{10.0*vit_scale}%** *bonus from DAILY fortunes (ignores bonus stacks)*\n' 
    vit_str += f' \u3000  \u3000  \u3000 **+{25*vitality}** *per BONUS stack, improves DAILY and CLAIM*'

    stamina = getStat(id, stats[1], BLOCKCHAIN)
    if stamina == 0: 
        sta_str = f'**+{0}** *additional daily WISH count (also reduces wish cost)*\n'
        sta_str += f' \u3000  \u3000  \u3000 **+{int(stamina/2)}** *additional weekly SUBMIT count*\n' 
        sta_str += f' \u3000  \u3000  \u3000 **+{int(stamina/3)}** *additional weekly CLAIM count*'
    else:
        sta_str = f'**+{int(stamina/2) + 1}** *additional daily WISH count*\n'
        sta_str += f' \u3000  \u3000  \u3000 **+{int(stamina/2)}** *additional weekly SUBMIT count*\n' 
        sta_str += f' \u3000  \u3000  \u3000 **+{int(stamina/3)}** *additional weekly CLAIM count*'

    strength = getStat(id, stats[2], BLOCKCHAIN)
    str_str = f'**+{50*strength}** *flat bonus to weekly SUBMIT bounty*\n'
    str_str += f' \u3000  \u3000  \u3000 **+{50*strength}** *flat bonus to increase weekly CLAIM bounty*'

    dexterity = getStat(id, stats[3], BLOCKCHAIN)
    if dexterity == 0:
        dex_str = f'**+{60*dexterity}%** *bonus from clip night REVIEW bounty*\n'
        dex_str += f' \u3000  \u3000  \u3000 **+{16*dexterity}%** *bonus from weekly CLAIM bounty*\n'
        dex_str += f' \u3000  \u3000  \u3000 **+{0}** *additional BONUS stack(s), improves DAILY and CLAIM*'
    else:
        dex_str = f'**+{60*dexterity}%** *bonus from clip night REVIEW bounty*\n'
        dex_str += f' \u3000  \u3000  \u3000 **+{16*dexterity}%** *bonus from weekly CLAIM bounty*\n'
        dex_str += f' \u3000  \u3000  \u3000 **+{int(stamina/2) + 1}** *additional BONUS stacks, improves DAILY and CLAIM*'

    ego = getStat(id, stats[4], BLOCKCHAIN)
    ego_str = f' **+{ego}** *Corrupted Reforger(s) to transform stars*\n'
    ego_str += f' \u3000  \u3000  \u3000 **+{20*ego}%** *of total creds as risk and reward on CONSUME*\n'
    ego_str += f' \u3000  \u3000  \u3000 **+{round(0.3*ego, 2)}%** *probability of pulling a* **Dark Star** *on WISH*'

    fortune = getStat(id, stats[5], BLOCKCHAIN)
    for_str = f'**+{0.5*fortune}%** *probability of pulling a* **Star** *on WISH*\n'
    for_str += f' \u3000  \u3000  \u3000 **+{0.8*fortune}%** *probability of pulling a* **Star** *on DAILY*\n'
    for_str += f' \u3000  \u3000  \u3000 **-{40*fortune}** *base cost of total wishes*'

    desc = f'Below lists your current student stats and benefits:\n\n'
    desc += f'**VIT {vitality}**\u3000{vit_str}\n'
    if vitality < 5: desc += f' \u3000  \u3000  \u3000 (NEXT: {1000 + 800*(vitality)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000 (MAX Level)\n\n'

    desc += f'**STA {stamina}**\u3000{sta_str}\n'
    if stamina < 5: desc += f' \u3000  \u3000  \u3000 (NEXT : {600 + 800*(stamina)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000 (MAX Level)\n\n'

    desc += f'**STR {strength}**\u3000{str_str}\n'
    if strength < 5: desc += f' \u3000  \u3000  \u3000 (NEXT: {700 + 650*(strength)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000 (MAX Level)\n\n'

    desc += f'**DEX {dexterity}**\u3000{dex_str}\n'
    if dexterity < 5: desc += f' \u3000  \u3000  \u3000 (NEXT: {1200 + 400*(dexterity)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000 (MAX Level)\n\n'

    desc += f'**EGO {ego} **\u2000 {ego_str}\n'
    if ego < 5: desc += f' \u3000  \u3000  \u3000 (NEXT: {2000})\n\n'
    else: desc += ' \u3000  \u3000  \u3000 (MAX Level)\n\n'

    desc += f'**FOR {fortune}**\u3000{for_str}\n'
    if fortune < 5: desc += f' \u3000  \u3000  \u3000 (NEXT: {500 + 900*(fortune)})\n\n'
    else: desc += ' \u3000  \u3000  \u3000 (MAX Level)\n\n'

    desc += f'You have **{star} Stars**, bring them to the Starforger with `/forge` to upgrade a core stat. \n\n'
    desc += f'You have **{reforger} Corrupted Reforgers**, you can use `/reforge` to turn **Stars** into **Dark Stars** and vice versa\n\n'
    desc += f'You have **{dark_star} Dark Stars**, you can activate them with `/consume` to gamble your creds, risk/reward is based on **EGO** \n\n'
    desc += f'Check out the Full Stat Sheet Here: https://discord.com/channels/859993171156140061/938853545992667176/1086749743193018513\n\n'

    """Return Message"""
    embed = discord.Embed(
        title = f'{name}\'s Stats',
        description = desc,
        color = 15814693,
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)
    return

async def upgrade (ctx, stat_name, BLOCKCHAIN):
    if disabledUpgrade(BLOCKCHAIN) == 1:
        """Return Message"""
        embed = discord.Embed(
            title = f'Upgrade',
            description = 'Upgrade is currently Disabled',
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    if stat_name.lower() == 'vitality' or stat_name.lower() == 'vit':
        await levelStat(ctx, 'Vitality', BLOCKCHAIN)
    if stat_name.lower() == 'stamina' or stat_name.lower() == 'sta':
        await levelStat(ctx, 'Stamina', BLOCKCHAIN)
    if stat_name.lower() == 'strength' or stat_name.lower() == 'str':
        await levelStat(ctx, 'Strength', BLOCKCHAIN)
    if stat_name.lower() == 'dexterity' or stat_name.lower() == 'dex':
        await levelStat(ctx, 'Dexterity', BLOCKCHAIN)
    if stat_name.lower() == 'ego':
        await levelStat(ctx, 'Ego', BLOCKCHAIN)
    if stat_name.lower() == 'fortune' or stat_name.lower() == 'for':
        await levelStat(ctx, 'Fortune', BLOCKCHAIN)

async def levelStat (ctx, stat_name, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name

    stat, cost = 0, 0
    if stat_name == 'Vitality':
        stat = getStat(id, stat_name, BLOCKCHAIN)
        cost = 1000 + 800*(stat)
    if stat_name == 'Stamina':
        stat = getStat(id, stat_name, BLOCKCHAIN)
        cost = 600 + 800*(stat)
    if stat_name == 'Strength':
        stat = getStat(id, stat_name, BLOCKCHAIN)
        cost = 700 + 650*(stat)
    if stat_name == 'Dexterity':
        stat = getStat(id, stat_name, BLOCKCHAIN)
        cost = 1200 + 400*(stat)
    if stat_name == 'Ego':
        stat = getStat(id, stat_name, BLOCKCHAIN)
        cost = 2000
    if stat_name == 'Fortune':
        stat = getStat(id, stat_name, BLOCKCHAIN)
        cost = 500 + 900*(stat)

    creds = user.totalCreds(id, BLOCKCHAIN)

    if stat >= 5:
        desc = f'Your **{stat_name}** is at MAX level, **STAR**s are required to reach the next level.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Level Up - {stat_name}',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    if creds < cost:
        desc = f'Insufficient funds. **{stat_name} {stat}** -> **{stat_name} {stat+1}** requires **{cost}** uwuCreds.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Level up - {stat_name}',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
    
    else: 
        """Generate new Block"""
        new_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = f'{stat_name}',
            data = -cost
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()

        if stat_name.lower() == 'ego':
            reforger_block = block.Block(
                user = id,
                name = name,
                timestamp = today(),
                description = 'Reforger',
                data = 0
            )
            BLOCKCHAIN.addBlock(reforger_block)
    
        BLOCKCHAIN.addBlock(new_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           

        desc = f'Congratulations. **{stat_name} {stat}** -> **{stat_name} {stat+1}**!!!\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Level up - {stat_name}',
            description = desc,
            color = 2352682,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return
    
def disabledUpgrade(BLOCKCHAIN) -> bool:
    if len(BLOCKCHAIN.chain) == 1: return True
    
    desc, count = 'Disable Upgrade', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getDesc() == desc:
            count += 1
                     
    print('count ', count)
    print('returning ', count%2)
    return count%2

async def wish (ctx, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name
    fortune = getStat(id, stats[5], BLOCKCHAIN)
    stamina = getStat(id, stats[1], BLOCKCHAIN)
    ego = getStat(id, stats[4])
    creds= user.totalCreds(id, BLOCKCHAIN)

    if stamina == 0: wish_count = 2 + int(stamina/2)
    else: wish_count = 2 + int(stamina/2) + 1

    cost = int(600 - 40*fortune)
    cost = int(cost/wish_count)
    if cost < 0: cost = 0

    if stamina == 0: wish_count = 2
    else: wish_count = 2 + int(stamina/2) + 1

    if user.hasWish(id, BLOCKCHAIN) >= wish_count:
        desc = f'You have no more Wishes left for today.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Wish Upon a Star',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    if creds < cost: 
        desc = f'Insufficient Funds. a wish costs **{cost}** uwuCreds.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Wish Upon a Star',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu, sponsored by Dre\'s Tears')
        await ctx.send(embed=embed)
        return
    
    star_flag = False
    wish_probability = 0.01 + 0.005*fortune
    if random.random() < wish_probability:
        star_flag = True

    dark_star_flag = False
    wish2_probability = 0.00 + 0.003*ego
    if random.random() < wish2_probability:
        dark_star_flag = True

    """Generate new Block"""
    new_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = f'Wish',
        data = -cost
    )

    star_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description= 'Star',
        data = 0
    )

    dark_star_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description= 'Dark Star',
        data = 0
    )
    
    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
 
    BLOCKCHAIN.addBlock(new_block)
    if star_flag: 
        BLOCKCHAIN.addBlock(star_block)
    if dark_star_flag:
        BLOCKCHAIN.addBlock(dark_star_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()

    if star_flag: 
        desc = f'Congratulations. You gained a **Star**!!!.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Wish Upon a Star',
            description = desc,
            color = 2352682,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://media0.giphy.com/media/hd1ilw50Zdb8Y/giphy.gif')
        embed.set_footer(text='@~ powered by UwUntu, sponsored by Dre\'s Tears')
        await ctx.send(embed=embed)
        return

    if dark_star_flag: 
        desc = f'Congratulations. You gained a **Dark Star**!!!.\n\n'

        """Return Message"""
        embed = discord.Embed(
            title = f'Wish Upon a Star',
            description = desc,
            color = 8388736,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://media.tenor.com/RUYUmoKQwQAAAAAd/pp-gif-cool.gif')
        embed.set_footer(text='@~ powered by UwUntu, sponsored by Dre\'s Tears')
        await ctx.send(embed=embed)
        return

    desc = f'You reached for the Stars, but they were too far.\n\n'

    """Return Message"""
    embed = discord.Embed(
        title = f'Wish Upon a Star',
        description = desc,
        color = 6053215,
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_image(url='https://media0.giphy.com/media/nWPLGmsjvdQ4g/giphy.gif')
    embed.set_footer(text='@~ powered by UwUntu, sponsored by Dre\'s Tears')
    await ctx.send(embed=embed)
    return

async def forge (ctx, stat_name, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name
    star = getStar(id, BLOCKCHAIN)

    if star <= 0:
        embed = discord.Embed(
            title = f'Starforger',
            description = f'The Starforger does not sense the power of a STAR within you, return once you have a STAR.',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    # Check Spelling
    stat, stat_level = '', 0
    if stat_name == 'vitality' or stat_name == 'Vitality' or stat_name == 'VIT' or stat_name == 'vit':
        stat = 'Vitality'
        stat_level = getStat(id, stats[0], BLOCKCHAIN) + 1
    if stat_name == 'stamina' or stat_name == 'Stamina' or stat_name == 'STA' or stat_name == 'sta':
        stat = 'Stamina'
        stat_level = getStat(id, stats[1], BLOCKCHAIN) + 1
    if stat_name == 'strength' or stat_name == 'Strength' or stat_name == 'STR' or stat_name == 'str':
        stat = 'Strength'
        stat_level = getStat(id, stats[2], BLOCKCHAIN) + 1
    if stat_name == 'dexterity' or stat_name == 'Dexterity' or stat_name == 'DEX' or stat_name == 'dex':
        stat = 'Dexterity'
        stat_level = getStat(id, stats[3], BLOCKCHAIN) + 1
    if stat_name == 'ego' or stat_name == 'Ego' or stat_name == 'EGO':
        stat = 'Ego'
        stat_level = getStat(id, stats[4], BLOCKCHAIN) + 1
    if stat_name == 'fortune' or stat_name == 'Fortune' or stat_name == 'FOR' or stat_name == 'for':
        stat = 'Fortune'
        stat_level = getStat(id, stats[5], BLOCKCHAIN) + 1

    """Generate new Block"""
    anti_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description = f'-Star',
        data = 0
    )

    stat_block = block.Block(
        user = id,
        name = name,
        timestamp = today(),
        description= stat,
        data = 0
    )

    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()

    if stat_name.lower() == 'ego':
        reforger_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'Reforger',
            data = 0
        )
        BLOCKCHAIN.addBlock(reforger_block)

    BLOCKCHAIN.addBlock(anti_block)
    BLOCKCHAIN.addBlock(stat_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain()
    
    desc = f'The Starforger shaped your STAR into **{stat} {stat_level}**.\n\n'

    """Return Message"""
    embed = discord.Embed(
        title = f'Starforger',
        description = desc,
        color = 2352682,
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_image(url='https://media.tenor.com/N9tfR3_w9uYAAAAC/gojo-satoru-hollow-purple.gif')
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)

async def reforge (ctx, item, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name

    reforger = getReforger(id, BLOCKCHAIN)
    if reforger <= 0:
        desc = f'You do not possess a **Corrupted Reforger**.'

        """Return Message"""
        embed = discord.Embed(
            title = f'Reforger',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://i.pinimg.com/originals/7b/02/82/7b0282a6b7054873ac77bca879261aeb.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    star = getStar(id, BLOCKCHAIN)
    dark_star = getDarkStar(id, BLOCKCHAIN)

    if item.lower() == 'star':
        if star <= 0:
            desc = f'You do not possess a **Star**.'

            """Return Message"""
            embed = discord.Embed(
                title = f'Reforger',
                description = desc,
                color = 6053215,
            ).set_thumbnail(url=ctx.author.avatar_url)
            embed.set_image(url='https://i.pinimg.com/originals/7b/02/82/7b0282a6b7054873ac77bca879261aeb.gif')
            embed.set_footer(text='@~ powered by UwUntu')
            await ctx.send(embed=embed)
            return
        
        star_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = '-Star',
            data = 0
        )
        
        dark_star_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'Dark Star',
            data = 0
        )

        reforger_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = '-Reforger',
            data = 0
        )

        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
        
        BLOCKCHAIN.addBlock(star_block)
        BLOCKCHAIN.addBlock(dark_star_block)
        BLOCKCHAIN.addBlock(reforger_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain() 

        desc = f'Your **Star** has corrupted into a **Dark Star**.'

        """Return Message"""
        embed = discord.Embed(
            title = f'Reforger',
            description = desc,
            color = 2352682,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://media.tenor.com/otlNc3em_hAAAAPo/limule-grand-sage.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    elif item.lower() == 'dark star':
        if dark_star <= 0:
            desc = f'You do not possess a **Dark Star**.'

            """Return Message"""
            embed = discord.Embed(
                title = f'Reforger',
                description = desc,
                color = 6053215,
            ).set_thumbnail(url=ctx.author.avatar_url)
            embed.set_image(url='https://i.pinimg.com/originals/7b/02/82/7b0282a6b7054873ac77bca879261aeb.gif')
            embed.set_footer(text='@~ powered by UwUntu')
            await ctx.send(embed=embed)
            return

        star_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'Star',
            data = 0
        )
        
        dark_star_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = '-Dark Star',
            data = 0
        )

        reforger_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = '-Reforger',
            data = 0
        )

        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
        
        BLOCKCHAIN.addBlock(star_block)
        BLOCKCHAIN.addBlock(dark_star_block)
        BLOCKCHAIN.addBlock(reforger_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain() 

        desc = f'Your **Dark Star** has reforged into a **Star**.'

        """Return Message"""
        embed = discord.Embed(
            title = f'Reforger',
            description = desc,
            color = 2352682,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://media.tenor.com/otlNc3em_hAAAAPo/limule-grand-sage.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    else:
        desc = f'Bad Item. Please input a **Star** to convert to a **Dark Star** or vice versa.'

        """Return Message"""
        embed = discord.Embed(
            title = f'Reforger',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

async def consume (ctx, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name

    dark_star = getDarkStar(id, BLOCKCHAIN)
    if dark_star <= 0:
        desc = f'You do not possess a **Dark Star** to consume.'

        """Return Message"""
        embed = discord.Embed(
            title = f'Consume',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://i.pinimg.com/originals/ec/e3/b3/ece3b3cd932f2a6f788f8259e4d205b5.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    user_creds = user.totalCreds(id, BLOCKCHAIN)
    if user_creds <= 0:
        desc = f'You do not possess a positive quantity of \'credits\', please resolve your poverty.'

        """Return Message"""
        embed = discord.Embed(
            title = f'Consume',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmFiYzRmYzQ2OGM2MzhlYmUxYjA3NzJjZTA5ZTdjODA0OTI1MTM2NiZjdD1n/zj0qdllevpf2w/giphy.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    ego = getStat(id, stats[4], BLOCKCHAIN)
    gamble = int(0.2*ego*user_creds)

    if random.random() < 0.4999999999997:
        gamble_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'Won the 50-50',
            data = gamble
        )

        desc = f'<@{id}> embraced the Beast of Darkness and gained **{gamble}** creds. (total: {user_creds + gamble})'

        """Return Message"""
        embed = discord.Embed(
            title = f'Consume',
            description = desc,
            color = 2352682,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://i.pinimg.com/originals/51/a2/46/51a246e425f9d28a643294f72c06b85f.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
    else:
        gamble_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'Lost the 50-50',
            data = -gamble
        )

        desc = f'<@{id}> was rejected by the Dark Star and lost **{gamble}** creds. (total: {user_creds - gamble})'

        """Return Message"""
        embed = discord.Embed(
            title = f'Consume',
            description = desc,
            color = 6053215,
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url='https://i.pinimg.com/originals/65/ae/27/65ae270df87c3c4adcea997e48f60852.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)

    dark_star = block.Block (
        user = id,
        name = name,
        timestamp = today(),
        description = '-Dark Star',
        data = 0
    )

    """Update Blockchain"""
    if BLOCKCHAIN.isChainValid() == False:
        print('The current Blockchain is not valid, performing rollback.')
        BLOCKCHAIN = blockchain.Blockchain()
    
    BLOCKCHAIN.addBlock(dark_star)
    BLOCKCHAIN.addBlock(gamble_block)
    if BLOCKCHAIN.isChainValid():
        BLOCKCHAIN.storeChain() 
    
    return

async def bless (ctx, reciever, client, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name

    """Parses Reciever id from <@id>"""
    reciever_id = reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

    if reciever_id == HBOT: reciever_id = HUMBLE

    """Check if the Giver is a god"""
    if id == ADMIN:

        """Generate new Block"""
        new_block = block.Block(
            user = reciever_id,
            name = await getName(reciever_id, client),
            timestamp = today(),
            description = f'Star',
            data = 0
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
        
        BLOCKCHAIN.addBlock(new_block)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           
            
        """Return Message"""
        embed = discord.Embed(
            title = f'Divine Blessing',
            description = f'A blessing from above. <@{reciever_id}> got a **Star**!',
            color = 16749300    
        ).set_image(url='https://www.ruru-berryz.com/wp-content/uploads/2017/01/Gabriel-DropOut-01-Pantsu.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
    else: 
        embed = discord.Embed(
            title = f'Divine Blessing',
            description = f'Insufficient power, you are not *god*!',
            color = 6053215    
        ).set_thumbnail(url='https://c.tenor.com/hal0bUXw_mYAAAAC/giyuu-tomioka-demon-slayer.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)

def getStat (user_id, stats, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, level = stats, 0
    desc1 = '-' + stats
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                level += 1
            if block.getDesc() == desc1:
                level -= 1
    return level

def getStar (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, desc1, level = 'Star', '-Star', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                level += 1
            if block.getDesc() == desc1:
                level -= 1
    return level

def getDarkStar (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, desc1, level = 'Dark Star', '-Dark Star', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                level += 1
            if block.getDesc() == desc1:
                level -= 1
    return level

def getReforger (user_id, BLOCKCHAIN)-> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc, desc1, level = 'Reforger', '-Reforger', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                level += 1
            if block.getDesc() == desc1:
                level -= 1
    return level