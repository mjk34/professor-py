import os
import random
import discord
from dotenv import load_dotenv

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from cmd import pong, halp, playlist, fetchMSG
from creds import daily, getCreds, getBd, handout, clearDatabase
from creds import purchase, give, setBirthday, checkBirthday, spy, uwuTax
from valorant import getScore, getSubmit, raffle
from mischief import dc

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
    '[MONTH DAY] | EXAMPLES: [JAN 1]   [01/01]   [01-01]',          # 7
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
    'How many uwuCreds will you spare?',                            # 19
    'Check the registered birthday date',                           # 20
    'Reward an user with uwuCreds, new creds',                      # 21
    'Peek at another memeber\'s uwuCred amount',                    # 22   
    'Take some creds from a specific misdemeanor',                  # 23
    'Calculate your Valorant game score and earn uwuCreds',         # 24
    'Number of kills you got in the game',                          # 25
    'Number of deaths you got in the game',                         # 26
    'Number of assists you got in the game',                        # 27
    'Number of multi kills you got in the game',                    # 28
    'Percent of head shot accuracy, use whole number',              # 29
    'Number of total rounds played',                                # 30
    'Check how many val-submits you have left',                     # 31
    'Spend 2000 + 400n uwuCreds to buy a raffle ticket',            # 32
    'Check your tickets for the current BP raffle'                  # 33
]

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    await client.change_presence(activity=discord.Game('UwU Try /help'))
    await checkBirthday(guild, client)

@client.event
async def on_message(message):
    if message.author == client.user: return        # checks if the sender is professor
    if message.author.id == GROOVY_ID: return       # checks if the sender is groovy
    if message.channel.id != CHANNEL: return        # checks if it comes from the bot channel

    # 3% change of get an uwu reply
    if random.random() < 0.12:
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

@slash.slash(name='iron', description=CMD_DESC[9], guild_ids=[GUILD_ID])#,
            # options=[create_option(name='victim', description=CMD_DESC[18], option_type=3, required=True)])
async def _iron(ctx:SlashContext, victim:str): 
    #await dc(ctx, victim, client)
    await purchase(ctx)

@slash.slash(name='bronze', description=CMD_DESC[10], guild_ids=[GUILD_ID])
async def _bronze(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='silver', description=CMD_DESC[11], guild_ids=[GUILD_ID])
async def _silver(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='gold', description=CMD_DESC[12], guild_ids=[GUILD_ID])
async def _gold(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='platinum', description=CMD_DESC[13], guild_ids=[GUILD_ID])
async def _platinum(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='ticket', description=CMD_DESC[32], guild_ids=[GUILD_ID])
async def _ticket(ctx:SlashContext): await purchase(ctx)

@slash.slash(name='uwu', description=CMD_DESC[14], guild_ids=[GUILD_ID])
async def _uwu(ctx:SlashContext): await daily(ctx)

@slash.slash(name='creds', description=CMD_DESC[15], guild_ids=[GUILD_ID])
async def _creds(ctx:SlashContext): await getCreds(ctx)

@slash.slash(name='give', description=CMD_DESC[17], guild_ids=[GUILD_ID],
             options=[create_option(name='receiver', description=CMD_DESC[18], option_type=3, required=True),
                      create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _give(ctx:SlashContext, receiver: str, amount: int): 
    await give(ctx, receiver, amount, client)

@slash.slash(name='getbd', description=CMD_DESC[20], guild_ids=[GUILD_ID])
async def _getbd(ctx:SlashContext): await getBd(ctx)

@slash.slash(name='handout', description=CMD_DESC[21], guild_ids=[GUILD_ID],
             options=[create_option(name='receiver', description=CMD_DESC[18], option_type=3, required=True),
                      create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _handout(ctx:SlashContext, receiver: str, amount: int): 
    await handout(ctx, receiver, amount, client)

@slash.slash(name='spy', description=CMD_DESC[22], guild_ids=[GUILD_ID],
             options=[create_option(name='target', description=CMD_DESC[18], option_type=3, required=True)])
async def _spy(ctx:SlashContext, target: str):
    await spy(ctx, target)

@slash.slash(name='uwutax', description=CMD_DESC[23], guild_ids=[GUILD_ID],
             options=[create_option(name='victim', description=CMD_DESC[18], option_type=3, required=True),
                      create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _uwutax(ctx:SlashContext, victim: str, amount: int):
    await uwuTax(ctx, victim, amount, client)

@slash.slash(name='getscore', description=CMD_DESC[24], guild_ids=[GUILD_ID],
             options=[create_option(name='kill', description=CMD_DESC[25], option_type=4, required=True),
                      create_option(name='death', description=CMD_DESC[26], option_type=4, required=True),
                      create_option(name='assist', description=CMD_DESC[27], option_type=4, required=True),
                      create_option(name='multi', description=CMD_DESC[28], option_type=4, required=True),
                      create_option(name='head', description=CMD_DESC[29], option_type=4, required=True),
                      create_option(name='rounds', description=CMD_DESC[30], option_type=4, required=True)])
async def _getscore(ctx:SlashContext, kill: int, death: int, assist: int, multi: int, head: int, rounds: int):
    await getScore(ctx, kill, death, assist, multi, head, rounds)

@slash.slash(name='getsubmit', description=CMD_DESC[31], guild_ids=[GUILD_ID])
async def _getSubmit(ctx:SlashContext):
    await getSubmit(ctx)

@slash.slash(name='iWANT2ERASE3v3ryTHING', description=CMD_DESC[16], guild_ids=[GUILD_ID])
async def _clear(ctx:SlashContext): await clearDatabase(ctx)

@slash.slash(name='raffle', description=CMD_DESC[33], guild_ids=[GUILD_ID])
async def _raffle(ctx:SlashContext):
    await raffle(ctx)

client.run(TOKEN)
