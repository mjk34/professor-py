import os, random, discord
import blockchain

from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from commands.cmd import ping, help
from commands.creds import daily, wallet, handout, take, snoop
from commands.gpt import gpt_string
from commands.helper import fetchContentList
from commands.valorant import getValScore

from commands.submit import buy_ticket, leaderboard, claimBonus, rafflelist


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('GUILD_ID'))

CHANNEL = int(os.getenv('BOT_CMD'))
GENERAL = int(os.getenv('GENERAL'))
SUBMIT = int(os.getenv('SUBMIT'))
DEVELOPER = int(os.getenv('DEVELOPER'))
PAWGERZ = int(os.getenv('PAWGERZ'))

CMD_DESC = fetchContentList('command.txt')

client = Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

keywords = ['ping', 'anime', 'uwu', 'wallet', 'give', 'handout', 'take', 'buy_ticket',\
            'bonus', 'leaderboard','clip', 'humble', 'raffle', 'stats', 'levelup', 'wish',\
            'review']

"""Either imports existing blockchain or initiates with a new genesis block"""
BLOCKCHAIN = blockchain.Blockchain('.Blockchain')

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
            # print(f'Pinged Professor: \"{content}\"')
            reply = await message.reply(f'{temp_msg[msg]}')
            gpt_str = await gpt_string('', content[len(token):])
            await reply.edit(content=gpt_str)
            return
    
    try:
        m_id = message.reference.message_id
        m_cid = message.reference.channel_id
        r_message = await client.get_channel(m_cid).fetch_message(m_id)

        m_aname = r_message.author.name
        m_context = r_message.content

        if m_aname == 'Professor':
            # print(f'Replying to Professor: \"{content}\"')
            reply = await message.reply(f'{temp_msg[msg]}')
            gpt_str = await gpt_string(m_context, content)
            await reply.edit(content=gpt_str)
            return
    except:
        return

    if message.channel.id == GENERAL:
        if token in content.lower():
            # print(f'Hey Professor: \"{content}\"')
            reply = await message.reply(f'{temp_msg[msg]}')
            gpt_str = await gpt_string('', content[len(token):])
            await reply.edit(content=gpt_str)
            return
        
        if random.random() < 0.05 and '?' in content:
            # print(f'Random Professor: \"{content}\"')
            gpt_str = await gpt_string('', content[len(token):])
            await client.get_channel(GENERAL).send(gpt_str)
            return

"""Non-Blockchain dependent commands"""
@slash.slash(name='ping', description=CMD_DESC[0], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await ping(ctx)

@slash.slash(name='help', description=CMD_DESC[38], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await help(ctx)

"""Blockchin dependent commands"""
@slash.slash(name='buy_ticket', description=CMD_DESC[3], guild_ids=[GUILD_ID],
    options=[create_option(name='amount', description=CMD_DESC[4], option_type=4, required=True)])
async def _(ctx:SlashContext, amount: int): 
    await buy_ticket(ctx, amount, BLOCKCHAIN)

@slash.slash(name='uwu', description=CMD_DESC[5], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await daily (ctx, BLOCKCHAIN)

@slash.slash(name='wallet', description=CMD_DESC[6], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await wallet(ctx, BLOCKCHAIN)

@slash.slash(name='handout', description=CMD_DESC[9], guild_ids=[GUILD_ID],
    options=[create_option(name='reciever', description=CMD_DESC[8], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[10], option_type=4, required=True)])
async def _(ctx:SlashContext, reciever: str, amount: int):
    reciever_list = reciever.split(',')
    for user in reciever_list:
        await handout(ctx, user, amount, client, BLOCKCHAIN)

@slash.slash(name='take', description=CMD_DESC[11], guild_ids=[GUILD_ID],
    options=[create_option(name='victim', description=CMD_DESC[8], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[10], option_type=4, required=True)])
async def _(ctx:SlashContext, victim: str, amount: int):
    await take(ctx, victim, amount, client, BLOCKCHAIN)
    
@slash.slash(name='submit_valorant', description="OG Valorant Submit", guild_ids=[GUILD_ID],
    options=[create_option(name='kill', description="how many kills", option_type=4, required=True),
             create_option(name='death', description="how many deaths", option_type=4, required=True),
             create_option(name='assist', description="how many assists", option_type=4, required=True),
             create_option(name='adr', description="average damage per round", option_type=4, required=True),
             create_option(name='head', description="head shot percent", option_type=4, required=True),
             create_option(name='rounds', description="how many rounds played", option_type=4, required=True)])
async def _(ctx:SlashContext, kill: int, death: int, assist: int, adr: int, head: int, rounds: int):
    await getValScore(ctx, kill, death, assist, adr, head, rounds, True, BLOCKCHAIN)

@slash.slash(name='leaderboard', description=CMD_DESC[15], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext):
    await leaderboard(ctx, BLOCKCHAIN)

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

client.run(TOKEN)