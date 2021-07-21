import os
import random
import discord
from dotenv import load_dotenv

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from cmd import pong, halp, playlist, fetchMSG
from creds import daily, getCreds, clearDatabase, getBd
from creds import purchase, give, setBirthday, checkBirthday

from uwuify import uwuify

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL = int(os.getenv('BOT_CMD'))
GROOVY_ID = int(os.getenv('GROOVY'))

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
    '[MONTH DAY] | EXAMPLES: [JAN 1]   [01/01]   [01-01]',                # 7
    'Spend 300 uwuCreds to submit an emoji to add to the server',   # 8
    'Spend 500 uwuCreds to submit a playlist to the /playlist list',# 9
    'Spend 1000 uwuCreds for help in code/valorant/study',          # 10
    'Spend 3000 uwuCreds for a custom painted profile icon',        # 11
    'Spend 7000 uwuCreds to apply for Moderator position',          # 12
    'Spend 10000 uwuCreds to request a small code or art project',  # 13
    'Collect your daily uwuCreds',                                  # 14
    'Check how many uwuCreds you have',                             # 15
    'DANGEROUS, WILL SNAP EVERYTHING',                              # 16
    'Feeling generous? Give your uwuCreds',                         # 17
    '[@<user name>] | EXAMPLES: @Dat1Weeaboo   @GreenRobotPanda',   # 18
    'How many uwuCreds will spare?',                                # 19
    'Check the registered birthday date',                           # 20
]

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    print(len(CMD_DESC))

    await client.change_presence(activity=discord.Game('UwU Try /help'))
    #await checkBirthday(guild, client)

@client.event
async def on_message(message):
    if message.author == client.user: return        # checks if the sender is professor
    if message.author.id == GROOVY_ID: return       # checks if the sender is groovy
    if message.channel.id != CHANNEL: return        # checks if it comes from the bot channel

    # 3% change of get an uwu reply
    if random.random() < 0.03:
        replace_message = uwuify(message.content)
        resend_message = f'{message.author.name}: ' + replace_message

        await message.delete()
        await client.get_channel(CHANNEL).send(resend_message)
    

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

@slash.slash(name='paper', description=CMD_DESC[8], guild_ids=[GUILD_ID])
async def _paper(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='iron', description=CMD_DESC[9], guild_ids=[GUILD_ID])
async def _iron(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='bronze', description=CMD_DESC[10], guild_ids=[GUILD_ID])
async def _bronze(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='silver', description=CMD_DESC[11], guild_ids=[GUILD_ID])
async def _silver(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='gold', description=CMD_DESC[12], guild_ids=[GUILD_ID])
async def _gold(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='platinum', description=CMD_DESC[13], guild_ids=[GUILD_ID])
async def platinum(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='uwu', description=CMD_DESC[14], guild_ids=[GUILD_ID])
async def _uwu(ctx:SlashContext): await daily(ctx)

@slash.slash(name='creds', description=CMD_DESC[15], guild_ids=[GUILD_ID])
async def _creds(ctx:SlashContext): await getCreds(ctx)

@slash.slash(name='clear', description=CMD_DESC[16], guild_ids=[GUILD_ID])
async def _clear(ctx:SlashContext): await clearDatabase(ctx)

@slash.slash(name='give', description=CMD_DESC[17], guild_ids=[GUILD_ID],
             options=[create_option(name='reciever', description=CMD_DESC[18], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _give(ctx:SlashContext, reciever: str, amount: int): 
    await give(ctx, reciever, amount, client)

@slash.slash(name='getbd', description=CMD_DESC[20], guild_ids=[GUILD_ID])
async def _getbd(ctx:SlashContext): await getBd(ctx)

client.run(TOKEN)
