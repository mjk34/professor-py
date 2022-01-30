import os, random, discord
import blockchain

from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from commands.cmd import ping, anime, uwuify
from commands.creds import daily, wallet, give, handout, take
from commands.valorant import buy_ticket, getValScore, bonusSubmit, leaderboard
from commands.helper import fetchContentList

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL = int(os.getenv('BOT_CMD'))
CMD_DESC = fetchContentList('command.txt')

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

"""Either imports existing blockchain or initiates with a new genesis block"""
BLOCKCHAIN = blockchain.Blockchain()

"""Start up bot status message on boot"""
@client.event
async def on_ready(): await client.change_presence(activity=discord.Game('testing /give'))

"""Filter message based on author and occasionally 'uwuify' read message"""
@client.event
async def on_message(message):
    if message.author == client.user: return        # checks if professor
    if message.channel.id != CHANNEL: return        # checks if from bot channel
    if random.random() < 0.01:                      # 15% chance to get uwufied
        replace_message = uwuify(message.content)
        resend_message = f'{message.author.name}: ' + replace_message
        
        await message.delete()
        await client.get_channel(CHANNEL).send(resend_message)    

"""Non-Blockchain dependent commands"""
@slash.slash(name='ping', description=CMD_DESC[0], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await ping(ctx)

@slash.slash(name='anime', description=CMD_DESC[4], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await anime(ctx)

"""Blockchin dependent commands"""
@slash.slash(name='buy_ticket', description=CMD_DESC[32], guild_ids=[GUILD_ID],
    options=[create_option(name='amount', description=CMD_DESC[36], option_type=4, required=True)])
async def _(ctx:SlashContext, amount: int): 
    await buy_ticket(ctx, amount, BLOCKCHAIN)

@slash.slash(name='uwu', description=CMD_DESC[14], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await daily (ctx, BLOCKCHAIN)

@slash.slash(name='wallet', description=CMD_DESC[15], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await wallet(ctx, BLOCKCHAIN)

@slash.slash(name='give', description=CMD_DESC[17], guild_ids=[GUILD_ID],
    options=[create_option(name='receiver', description=CMD_DESC[18], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _(ctx:SlashContext, receiver: str, amount: int): 
    await give(ctx, receiver, amount, client, BLOCKCHAIN)

@slash.slash(name='handout', description=CMD_DESC[21], guild_ids=[GUILD_ID],
    options=[create_option(name='receiver', description=CMD_DESC[18], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _(ctx:SlashContext, receiver: str, amount: int): 
    await handout(ctx, receiver, amount, client, BLOCKCHAIN)

@slash.slash(name='take', description=CMD_DESC[23], guild_ids=[GUILD_ID],
    options=[create_option(name='victim', description=CMD_DESC[18], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _(ctx:SlashContext, victim: str, amount: int):
    await take(ctx, victim, amount, client, BLOCKCHAIN)

@slash.slash(name='submit_valorant', description=CMD_DESC[24], guild_ids=[GUILD_ID],
    options=[create_option(name='kill', description=CMD_DESC[25], option_type=4, required=True),
             create_option(name='death', description=CMD_DESC[26], option_type=4, required=True),
             create_option(name='assist', description=CMD_DESC[27], option_type=4, required=True),
             create_option(name='adr', description=CMD_DESC[28], option_type=4, required=True),
             create_option(name='head', description=CMD_DESC[29], option_type=4, required=True),
             create_option(name='rounds', description=CMD_DESC[30], option_type=4, required=True)])
async def _(ctx:SlashContext, kill: int, death: int, assist: int, adr: int, head: int, rounds: int):
    await getValScore(ctx, kill, death, assist, adr, head, rounds, True, BLOCKCHAIN)
    
@slash.slash(name='view_valorant', description=CMD_DESC[24], guild_ids=[GUILD_ID],
    options=[create_option(name='kill', description=CMD_DESC[25], option_type=4, required=True),
             create_option(name='death', description=CMD_DESC[26], option_type=4, required=True),
             create_option(name='assist', description=CMD_DESC[27], option_type=4, required=True),
             create_option(name='adr', description=CMD_DESC[28], option_type=4, required=True),
             create_option(name='head', description=CMD_DESC[29], option_type=4, required=True),
             create_option(name='rounds', description=CMD_DESC[30], option_type=4, required=True)])
async def _(ctx:SlashContext, kill: int, death: int, assist: int, adr: int, head: int, rounds: int):
    await getValScore(ctx, kill, death, assist, adr, head, rounds, False, BLOCKCHAIN)

@slash.slash(name='leaderboard', description=CMD_DESC[34], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext):
    await leaderboard(ctx, BLOCKCHAIN)

@slash.slash(name='bonus_submit', description=CMD_DESC[35], guild_ids=[GUILD_ID],
    options=[create_option(name='reciever', description=CMD_DESC[18], option_type=3, required=True)])
async def _(ctx:SlashContext, reciever: str): 
    await bonusSubmit(ctx, reciever, client, BLOCKCHAIN)

client.run(TOKEN)