import os
import discord
from dotenv import load_dotenv

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from cmd import pong, halp, playlist, fetchMSG
from creds import daily, getCreds, clearDatabase, getBd
from creds import purchase, give, setBirthday, checkBirthday

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL = int(os.getenv('BOT_CMD'))

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

CMD_DESC = [
    'Pitch a ping',                                                 # 0
    'Get a list of my commands',                                    # 1
    'Show a list of music playlists',                               # 2
    'Show Dat1Weeaboo\'s MyAnimeList',                              # 3
    'Show Seasonal anime airing right now',                         # 4
    'Show a list of rewards you can purchase using uwuCreds',       # 5
    'Set your birthday, wait and see what happens',                 # 6
    '[MONTH DAY] | EXAMPLES: JAN 1   01/01   01-01',                # 7
    'Spend 1000 uwuCreds for that coding or math tutoring',         # 8
    'Spend 2000 uwuCreds for that valorant coaching or RR boost',   # 9
    'Spend 5000 uwuCreds for that custom profile icon',             # 10
    'Spend 10000 uwuCreds for that full body character design',     # 11
    'Collect your daily uwuCreds',                                  # 12
    'Check how many uwuCreds you have',                             # 13
    'DANGEROUS, WILL SNAP EVERYTHING',                              # 14
    'Feeling generous? Give your uwuCreds',                         # 15
    '[@<user name>] | EXAMPLES: @Dat1Weeaboo   @GreenRobotPanda',   # 16
    'How many uwuCreds will spare?',                                # 17
    'Check the registered birthday date',                           # 18
]

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    print(len(CMD_DESC))

    await client.change_presence(activity=discord.Game('/help'))
    await checkBirthday(guild, client)

@slash.slash(name='ping', description=CMD_DESC[0], guild_ids=[GUILD_ID])
async def _hello(ctx:SlashContext): await pong(ctx)

@slash.slash(name='help', description=CMD_DESC[1], guild_ids=[GUILD_ID])
async def _help(ctx:SlashContext): await halp(ctx)

@slash.slash(name='playlist', description=CMD_DESC[2], guild_ids=[GUILD_ID])
async def _playlist(ctx:SlashContext): await playlist(ctx)

@slash.slash(name='mal', description=CMD_DESC[3], guild_ids=[GUILD_ID])
async def _mal(ctx:SlashContext): await fetchMSG(ctx)

@slash.slash(name='anichart', description=CMD_DESC[4], guild_ids=[GUILD_ID])
async def _anichart(ctx:SlashContext): await fetchMSG(ctx)

@slash.slash(name='rewards', description=CMD_DESC[5], guild_ids=[GUILD_ID])
async def _mal(ctx:SlashContext): await fetchMSG(ctx)

# uwuCreds commands that uses the database
@slash.slash(name='setbd', description=CMD_DESC[6], guild_ids=[GUILD_ID],
             options=[create_option(name='birth_date', description=CMD_DESC[7], option_type=3, required=True)])

async def _setbd(ctx:SlashContext, birth_date: str):
    await setBirthday(ctx, birth_date)

@slash.slash(name='bronze', description=CMD_DESC[8], guild_ids=[GUILD_ID])
async def _bronze(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='silver', description=CMD_DESC[9], guild_ids=[GUILD_ID])
async def _silver(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='gold', description=CMD_DESC[10], guild_ids=[GUILD_ID])
async def _gold(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='platinum', description=CMD_DESC[11], guild_ids=[GUILD_ID])
async def platinum(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='uwu', description=CMD_DESC[12], guild_ids=[GUILD_ID])
async def _uwu(ctx:SlashContext): await daily(ctx)

@slash.slash(name='creds', description=CMD_DESC[13], guild_ids=[GUILD_ID])
async def _creds(ctx:SlashContext): await getCreds(ctx)

@slash.slash(name='clear', description=CMD_DESC[14], guild_ids=[GUILD_ID])
async def _clear(ctx:SlashContext): await clearDatabase(ctx)

@slash.slash(name='give', description=CMD_DESC[15], guild_ids=[GUILD_ID],
             options=[create_option(name='reciever', description=CMD_DESC[16], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[17], option_type=4, required=True)])
async def _give(ctx:SlashContext, reciever: str, amount: int): 
    await give(ctx, reciever, amount, client)

@slash.slash(name='getbd', description=CMD_DESC[18], guild_ids=[GUILD_ID])
async def _getbd(ctx:SlashContext): await getBd(ctx)

client.run(TOKEN)
