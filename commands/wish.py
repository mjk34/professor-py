import random, discord, block
import commands.user as user

from discord.utils import get

from commands.helper import today, getName
from commands.manager import pushBlock, pushWish

filler = ['<', '>', '!', '@', '&']

async def wish(ctx, mode, BLOCKCHAIN):
    id, name = ctx.author.id, ctx.author.name

    """Check for wish mode"""
    wish_count = user.wishCount(id, BLOCKCHAIN)
    max_iteration = 0
    if mode.lower() == 'single' or mode.lower() == 's' or mode.lower() == 'sin':
        """Check if user has at least 1 wish"""
        if wish_count < 1: 
            embed = discord.Embed(
                title = f'Wish',
                description = f'Insufficient wishes. Require at least 1 wish for a Single Pull. (wish count: {wish_count}).',
                color = 6053215    
            ).set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text='@~ powered by UwUntu')
            await ctx.send(embed=embed)
            return
        else: max_iteration = 1

    elif mode.lower() == 'multi' or mode.lower() == 'm':
        """Check if user has at least 10 wish"""
        if wish_count < 10: 
            embed = discord.Embed(
                title = f'Wish',
                description = f'Insufficient wishes. Require at least 10 wishes for a Multi Pull. (wish count: {wish_count}).',
                color = 6053215    
            ).set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text='@~ powered by UwUntu')
            await ctx.send(embed=embed)
            return
        else: max_iteration = 10

    else:
        embed = discord.Embed(
            title = f'Wish',
            description = f'Please use \'Single\' for 1 pull and \'Multi\' for 10 pulls...',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    items_pulled, scrap_sum = [], 0
    for i in range(max_iteration):
        star_pity = getStarPity(id, BLOCKCHAIN)
        item_pity = getItemPity(id, BLOCKCHAIN)
        check = guarenteed(id, BLOCKCHAIN)

        item = pull(star_pity, item_pity, check)
        item_desc = ', '.join(item)

        """Generate Pull Block"""
        pull_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = item_desc,
            data = 0
        )

        """Generate Item Block"""
        content, server_bonus = 0, user.getServerBonus(BLOCKCHAIN)
        if item[2] == 'Cred Bag': content = 300 * (server_bonus + 1)
        if item[1] == '0*': 
            content = random.randint(10, 25)
                    
        item_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = item[2],
            data = content
        )

        """Generate Wish Block"""
        wish_block = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = '-Wish',
            data = 0
        )

        pushBlock(pull_block, BLOCKCHAIN)
        pushBlock(item_block, BLOCKCHAIN)
        pushBlock(wish_block, BLOCKCHAIN)

        if max_iteration == 1:
            desc, color, gif = '', -1, ''
            if item[1] == '5*':
                desc = f'Holy Shit! A Star Descends!\n\n'
                desc += f'**1x {item[2]} {text2Emoji(item[2])}**'
                color = 16700447
                gif = 'https://media.tenor.com/Z5kE_QEkGdgAAAAC/roll-wishing.gif'
            elif item[1] == '4*':
                desc = f'You reached for the Stars, and found something!\n\n**1x {item[2]} {text2Emoji(item[2])}**.'
                color = 10027263
                gif = 'https://media.tenor.com/8OqlJIRATS0AAAAC/wishing-genshin.gif'
            else:
                desc = f'You reached for the Stars, but they were too far.\n\nYou got **{content} Creds**.'
                color = 6053215
                gif = 'https://media0.giphy.com/media/nWPLGmsjvdQ4g/giphy.gif'

            """Return Message"""
            embed = discord.Embed(
                title = 'Single Wish',
                description = desc,
                color = color    
            ).set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text='@~ powered by UwUntu, sponsored by Dre\'s tears')
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
            return
        else:
            items_pulled.append(item)
            scrap_sum += content
    
    """Get highest rarity"""
    desc, color, gif = '', -1, ''
    rarity = getHighestRarity(items_pulled)

    if rarity == '5*':
        desc = f'You reached for the Stars... and got a Star!\n\n**'
        color = 16700447
        gif = 'https://media.tenor.com/Z5kE_QEkGdgAAAAC/roll-wishing.gif'
    else:
        desc = f'You reached for the Stars... and saw the light!\n\n**'
        color = 10027263
        gif = 'https://media.tenor.com/8OqlJIRATS0AAAAC/wishing-genshin.gif'


    for i in range(len(items_pulled)):
        if items_pulled[i][1] == '4*' or items_pulled[i][1] == '5*':
            desc += f'1x {items_pulled[i][2]} {text2Emoji(items_pulled[i][2])}\n'
    desc += '**\n'

    """Return Message"""
    embed = discord.Embed(
        title = 'Multi Wish',
        description = desc,
        color = color    
    ).set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='@~ powered by UwUntu, sponsored by Dre\'s tears')
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

def text2Emoji(item):
    if item == 'Cred Bag': return '💰'
    if item == 'Token': return '🪙'
    if item == 'Torn Ticket': return '🎫'
    if item == 'Bonus Submit': return '🎞️'
    if item == 'Reforger': return '🔨'
    if item == 'Star': return '⭐'
    if item == 'Dark Star': return '💥'

def getHighestRarity(item_list) -> str:
    for item in item_list:
        if item[1] == '5*': return '5*'

    return '4*'

def randomItem() -> str:
    items = ['Cred Bag', 'Torn Ticket', 'Reforger']
    index = random.randint(0, len(items)-1)

    return items[index]

def pull(total_pity, pity, guarenteed) -> list:
    
    # 5* probability check -------------------------------------
    item = None
    if total_pity < 73:
        if random.random() < 0.006:
            # Hit the 5*, WOOOT
            if guarenteed:
                item = ['Pull', '5*', 'Star'] 
            elif random.random() < 0.5:
                item = ['Pull', '5*', 'Star']
            else:
                item = ['Pull', '5*', 'Dark Star']
        
    if total_pity >= 73 and total_pity < 89:
        probability = 0.006 + 0.06*(total_pity - 72)
        if random.random() < probability:
            # Hit the 5*, less WOOOT
            if guarenteed:
                item = ['Pull', '5*', 'Star'] 
            elif random.random() < 0.5:
                item = ['Pull', '5*', 'Star']
            else:
                item = ['Pull', '5*', 'Dark Star']

    if total_pity == 89:
        # Hit the 5*, fucking hell
        if guarenteed:
            item = ['Pull', '5*', 'Star'] 
        elif random.random() < 0.5:
            item = ['Pull', '5*', 'Star']
        else:
            item = ['Pull', '5*', 'Dark Star']

    if item is not None:
        return item

    # 4* probability check -------------------------------------
    if pity < 8:
        if random.random() < 0.051:
            # Hit the 4*, WOOOT
            if random.random() < 0.45:
                item = ['Pull', '4*', 'Token']
            elif random.random() >= 0.45 and random.random() < 0.5:
                item = ['Pull', '4*', 'Bonus Submit']
            else:
                item = ['Pull', '4*', randomItem()]

    if pity == 8:
        if random.random() < 0.561:
            # Hit the 4*, less WOOOT
            if random.random() < 0.45:
                item = ['Pull', '4*', 'Token']
            elif random.random() >= 0.45 and random.random() < 0.5:
                item = ['Pull', '4*', 'Bonus Submit']
            else:
                item = ['Pull', '4*', randomItem()]

    if pity > 8:
        # Hit the 4*, fucking hell
        if random.random() < 0.45:
            item = ['Pull', '4*', 'Token']
        elif random.random() >= 0.45 and random.random() < 0.5:
                item = ['Pull', '4*', 'Bonus Submit']
        else:
            item = ['Pull', '4*', randomItem()]

    if item is not None:
        return item
    else:
        return ['Pull', '0*', '']

async def give_wish(ctx, reciever, amount, client, BLOCKCHAIN):

    """Check of amount is less than 1"""
    if amount < 1:
        embed = discord.Embed(
            title = f'Bonus Wish',
            description = f'You cannot give {amount} wishes.',
            color = 6053215    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        return

    """Parses Reciever id from <@id>"""
    reciever_id = reciever
    for ch in filler: reciever_id = reciever_id.replace(ch, '')
    reciever_id = int(reciever_id)

    reciever_name = await getName(reciever_id, client)

    """Check if the Giver is a moderator"""
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        
        for i in range(amount):
            pushWish(reciever_id, reciever_name, BLOCKCHAIN)
        
        """Return Message"""
        embed = discord.Embed(
            title = f'Bonus Wish',
            description = f'**{amount}** Wishes were added to <@{reciever_id}>\'s *Wallet*!',
            color = 16749300    
        ).set_image(url='https://media.tenor.com/lfYGrPJlQLAAAAAC/oshi-no-ko-ruby.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(f'<@{reciever_id}>', embed=embed)
    else: 
        embed = discord.Embed(
            title = f'Handout',
            description = f'Insufficient power, you are not a moderator!',
            color = 6053215    
        ).set_thumbnail(url='https://media1.tenor.com/images/80662c4e35cf12354f65f1d6f7beada8/tenor.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)

def getStarPity(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc1, desc2, desc3, total_pity = '5*', '4*', '0*', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if len(block.getDesc().split(', ')) == 3:
                rarity = block.getDesc().split(', ')[1]

                if rarity == desc1:
                    total_pity = 0
                elif rarity == desc2:
                    total_pity += 1
                elif rarity == desc3:
                    total_pity += 1
                else: continue
                        
    return total_pity

def getItemPity(user_id, BLOCKCHAIN) -> int:
    if len(BLOCKCHAIN.chain) == 1: return 0

    desc1, desc2, desc3, item_pity = '5*', '4*', '0*', 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if len(block.getDesc().split(', ')) == 3:
                rarity = block.getDesc().split(', ')[1]

                if rarity == desc1:
                    item_pity += 1
                elif rarity == desc2:
                    item_pity = 0
                elif rarity == desc3:
                    item_pity += 1
                else: continue
                        
    return item_pity

def guarenteed(user_id, BLOCKCHAIN) -> bool:
    if len(BLOCKCHAIN.chain) == 1: return False

    guarenteed, desc1, desc2 = False, '5*', 'Dark Star'
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if len(block.getDesc().split(', ')) == 3:
                if block.getDesc().split(', ')[1] == desc1:
                    if block.getDesc().split(', ')[2] == desc2:
                        guarenteed = True
                    else:
                        guarenteed = False
    
    return guarenteed