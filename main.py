import os, random, discord
import blockchain

from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from commands.cmd import ping, anime, pong
from commands.creds import daily, wallet, give, handout, take, snoop
from commands.games import submitClip, review
from commands.submit import buy_ticket, bonusSubmit, leaderboard, claimBonus, rafflelist
from commands.helper import fetchContentList
from commands.humble import humble_powa
from commands.gpt import gpt_string
from commands.stats import profile, upgrade, wish, forge, bless, reforge, consume
from commands.god import hand_all, take_level, give_level

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL = int(os.getenv('BOT_CMD'))
GENERAL = int(os.getenv('GENERAL'))
CMD_DESC = fetchContentList('command.txt')

client = Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

keywords = ['ping', 'anime', 'uwu', 'wallet', 'give', 'handout', 'take', 'buy_ticket',\
            'bonus', 'leaderboard','clip', 'humble', 'raffle', 'stats', 'levelup', 'wish',\
            'review']

"""Either imports existing blockchain or initiates with a new genesis block"""
BLOCKCHAIN = blockchain.Blockchain()

"""Start up bot status message on boot"""
@client.event
async def on_ready(): await client.change_presence(activity=discord.Game('/uwu for fortune!'))

"""Filter message based on author and occasionally 'uwuify' read message"""
@client.event
async def on_message(message):
    if message.author.name in ['Assistant', 'Professor', 'humble', 'valuwu', 'RoleBot']: return
    if message.author == client.user: return                # checks if professor  
    if message.content.split(' ')[0] in keywords: return    # checks for keywords (commands)

    content = message.content
    temp_msg = ['Typing...', 'Ummm...', 'Hmmm...', 'Thinking...']
    msg = random.randint(0, 3)

    ping = '<@787353505132183592>'
    token = 'hey professor'
    if ping in content:
            print(f'Pinged Professor: \"{content}\"')
            reply = await message.reply(f'{temp_msg[msg]}')
            gpt_str = await gpt_string('', content[len(token):])
            await reply.edit(content=gpt_str)
            return
    
    print('\ncheck 1')
    try:
        print('check 2')
        m_id = message.reference.message_id
        m_cid = message.reference.channel_id
        r_message = await client.get_channel(m_cid).fetch_message(m_id)

        m_aname = r_message.author.name
        m_context = r_message.content
        print(m_aname)
        if m_aname == 'Professor':
            print(f'Replying to Professor: \"{content}\"')
            reply = await message.reply(f'{temp_msg[msg]}')
            gpt_str = await gpt_string(m_context, content)
            await reply.edit(content=gpt_str)
            return
    except:
        print('check 3')
        return

    if message.channel.id == GENERAL:
        if token in content.lower():
            print(f'Hey Professor: \"{content}\"')
            reply = await message.reply(f'{temp_msg[msg]}')
            gpt_str = await gpt_string('', content[len(token):])
            await reply.edit(content=gpt_str)
            return
        
        if random.random() < 0.75 and '?' in content:
            print(f'Random Professor: \"{content}\"')
            gpt_str = await gpt_string('', content[len(token):])
            await client.get_channel(GENERAL).send(gpt_str)
            return

"""Non-Blockchain dependent commands"""
@slash.slash(name='ping', description=CMD_DESC[0], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await ping(ctx)

@slash.slash(name='pong', description=CMD_DESC[1], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await pong(ctx)

@slash.slash(name='anime', description=CMD_DESC[2], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await anime(ctx)

"""Blockchin dependent commands"""
@slash.slash(name='buy_ticket', description=CMD_DESC[3], guild_ids=[GUILD_ID],
    options=[create_option(name='amount', description=CMD_DESC[4], option_type=4, required=True)])
async def _(ctx:SlashContext, amount: int): 
    await buy_ticket(ctx, amount, BLOCKCHAIN)

@slash.slash(name='uwu', description=CMD_DESC[5], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): 
    await daily (ctx, client, BLOCKCHAIN)
    await humble_powa (ctx, client, BLOCKCHAIN)

@slash.slash(name='wallet', description=CMD_DESC[6], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await wallet(ctx, BLOCKCHAIN)

@slash.slash(name='donate', description=CMD_DESC[7], guild_ids=[GUILD_ID],
    options=[create_option(name='receiver', description=CMD_DESC[8], option_type=3, required=True)])
async def _(ctx:SlashContext, receiver: str): 
    await give(ctx, receiver, client, BLOCKCHAIN)

@slash.slash(name='handout', description=CMD_DESC[9], guild_ids=[GUILD_ID],
    options=[create_option(name='receiver', description=CMD_DESC[8], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[10], option_type=4, required=True)])
async def _(ctx:SlashContext, receiver: str, amount: int): 
    await handout(ctx, receiver, amount, client, BLOCKCHAIN)

# create handoutmulti for multiple users

@slash.slash(name='take', description=CMD_DESC[11], guild_ids=[GUILD_ID],
    options=[create_option(name='victim', description=CMD_DESC[8], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[10], option_type=4, required=True)])
async def _(ctx:SlashContext, victim: str, amount: int):
    await take(ctx, victim, amount, client, BLOCKCHAIN)

# create takemulti for multiple users

@slash.slash(name='submit_clip', description=CMD_DESC[12], guild_ids=[GUILD_ID],
    options=[create_option(name='title', description=CMD_DESC[13], option_type=3, required=True),
             create_option(name='link', description=CMD_DESC[14], option_type=3, required=True)])
async def _(ctx:SlashContext, title: str, link: str):
    await submitClip(ctx, title, link, BLOCKCHAIN)
    
@slash.slash(name='leaderboard', description=CMD_DESC[15], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext):
    await leaderboard(ctx, BLOCKCHAIN)

@slash.slash(name='give_submit', description=CMD_DESC[16], guild_ids=[GUILD_ID],
    options=[create_option(name='reciever', description=CMD_DESC[8], option_type=3, required=True)])
async def _(ctx:SlashContext, reciever: str): 
    await bonusSubmit(ctx, reciever, client, BLOCKCHAIN)

@slash.slash(name='claim_bonus', description=CMD_DESC[17], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await claimBonus(ctx, BLOCKCHAIN)

@slash.slash(name='raffle', description=CMD_DESC[18], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await rafflelist(ctx, BLOCKCHAIN)

@slash.slash(name='snoop', description=CMD_DESC[19], guild_ids=[GUILD_ID],
    options=[create_option(name='target', description=CMD_DESC[8], option_type=3, required=True)])
async def _(ctx:SlashCommand, target: str):
    await snoop(ctx, target, client, BLOCKCHAIN)

@slash.slash(name="profile", description=CMD_DESC[20], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await profile(ctx, BLOCKCHAIN)

@slash.slash(name='upgrade', description=CMD_DESC[21], guild_ids=[GUILD_ID],
    options=[create_option(name='stat', description=CMD_DESC[22], option_type=3, required=True)])
async def _(ctx:SlashCommand, stat: str):
    await upgrade(ctx, stat, BLOCKCHAIN)

# rework wish into its own file
@slash.slash(name='wish', description=CMD_DESC[23], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await wish(ctx, BLOCKCHAIN)

@slash.slash(name='forge', description=CMD_DESC[24], guild_ids=[GUILD_ID],
    options=[create_option(name='stat', description=CMD_DESC[22], option_type=3, required=True)])
async def _(ctx:SlashCommand, stat: str):
    await forge(ctx, stat, BLOCKCHAIN)

@slash.slash(name='reforge', description=CMD_DESC[25], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await reforge(ctx, BLOCKCHAIN)

@slash.slash(name='consume', description=CMD_DESC[26], guild_ids=[GUILD_ID],
    options=[create_option(name='amount', description=CMD_DESC[27], option_type=4, required=True)])
async def _(ctx:SlashCommand, amount:int):
    await consume(ctx, amount, BLOCKCHAIN)

@slash.slash(name='review', description=CMD_DESC[28], guild_ids=[GUILD_ID],
    options=[create_option(name='reciever', description=CMD_DESC[8], option_type=3, required=True),
             create_option(name='rating', description=CMD_DESC[29], option_type=4, required=True)])
async def _(ctx:SlashCommand, reciever: str, rating: int):
    await review(ctx, reciever, rating, client, BLOCKCHAIN)

"""Special Case Commands"""
@slash.slash(name='bless', description=CMD_DESC[30], guild_ids=[GUILD_ID],
    options=[create_option(name='reciever', description=CMD_DESC[8], option_type=3, required=True)])
async def _(ctx:SlashCommand, reciever: str):
    await bless(ctx, reciever, client, BLOCKCHAIN)

@slash.slash(name='hand_all', description=CMD_DESC[31], guild_ids=[GUILD_ID],
    options=[create_option(name='amount', description=CMD_DESC[10], option_type=4, required=True)])
async def _(ctx:SlashCommand, amount: int):
    await hand_all(ctx, amount, client, BLOCKCHAIN)

@slash.slash(name='take_level', description=CMD_DESC[32], guild_ids=[GUILD_ID],
    options=[create_option(name='target', description=CMD_DESC[8], option_type=3, required=True),
             create_option(name='stat', description=CMD_DESC[22], option_type=3, required=True)])
async def _(ctx:SlashCommand, target:str, stat:str):
    await take_level(ctx, target, stat, client, BLOCKCHAIN)

@slash.slash(name='give_level', description=CMD_DESC[33], guild_ids=[GUILD_ID],
    options=[create_option(name='target', description=CMD_DESC[1], option_type=3, required=True),
             create_option(name='stat', description=CMD_DESC[22], option_type=3, required=True)])
async def _(ctx:SlashCommand, target:str, stat:str):
    await give_level(ctx, target, stat, client, BLOCKCHAIN)

client.run(TOKEN)