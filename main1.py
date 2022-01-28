import os, random, discord

from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from cmd    import pong, halp, playlist, fetchMSG
from creds  import daily, getCreds, handout, clearDatabase
from creds  import purchase, give, spy, uwuTax
from valsub import getScore, getSubmit, raffle, leaderboard, restoreSubmit
from uwuify import uwuify
from helper import fetchCMD

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL = int(os.getenv('BOT_CMD'))
GROOVY_ID = int(os.getenv('GROOVY'))
CMD_DESC = fetchCMD()

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready(): await client.change_presence(activity=discord.Game('#UwU /help'))

@client.event
async def on_message(message):
    if message.author == client.user: return        # checks if professor
    if message.author.id == GROOVY_ID: return       # checks if groovy
    if message.channel.id != CHANNEL: return        # checks if from bot channel
    if random.random() < 0.12: # 12% chance to get uwufied
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

@slash.slash(name='anichart', description=CMD_DESC[4], guild_ids=[GUILD_ID])
async def _anichart(ctx:SlashContext): await fetchMSG(ctx)

# uwuCreds commands that uses the database
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

@slash.slash(name='submitGame', description=CMD_DESC[24], guild_ids=[GUILD_ID],
             options=[create_option(name='kill', description=CMD_DESC[25], option_type=4, required=True),
                      create_option(name='death', description=CMD_DESC[26], option_type=4, required=True),
                      create_option(name='assist', description=CMD_DESC[27], option_type=4, required=True),
                      create_option(name='adr', description=CMD_DESC[28], option_type=4, required=True),
                      create_option(name='head', description=CMD_DESC[29], option_type=4, required=True),
                      create_option(name='rounds', description=CMD_DESC[30], option_type=4, required=True)])
async def _submitGame(ctx:SlashContext, kill: int, death: int, assist: int, adr: int, head: int, rounds: int):
    await getScore(ctx, kill, death, assist, adr, head, rounds, True)
    
@slash.slash(name='viewGame', description=CMD_DESC[24], guild_ids=[GUILD_ID],
             options=[create_option(name='kill', description=CMD_DESC[25], option_type=4, required=True),
                      create_option(name='death', description=CMD_DESC[26], option_type=4, required=True),
                      create_option(name='assist', description=CMD_DESC[27], option_type=4, required=True),
                      create_option(name='adr', description=CMD_DESC[28], option_type=4, required=True),
                      create_option(name='head', description=CMD_DESC[29], option_type=4, required=True),
                      create_option(name='rounds', description=CMD_DESC[30], option_type=4, required=True)])
async def _viewGame(ctx:SlashContext, kill: int, death: int, assist: int, adr: int, head: int, rounds: int):
    await getScore(ctx, kill, death, assist, adr, head, rounds, False)

@slash.slash(name='getsubmit', description=CMD_DESC[31], guild_ids=[GUILD_ID])
async def _getSubmit(ctx:SlashContext):
    await getSubmit(ctx)

@slash.slash(name='iWANT2ERASE3v3ryTHING', description=CMD_DESC[16], guild_ids=[GUILD_ID])
async def _clear(ctx:SlashContext): await clearDatabase(ctx)

@slash.slash(name='raffle', description=CMD_DESC[33], guild_ids=[GUILD_ID])
async def _raffle(ctx:SlashContext):
    await raffle(ctx)

@slash.slash(name='leaderboard', description=CMD_DESC[34], guild_ids=[GUILD_ID])
async def _leaderboard(ctx:SlashContext):
    await leaderboard(ctx)
    
@slash.slash(name='restoreSubmit', description=CMD_DESC[35], guild_ids=[GUILD_ID],
            options=[create_option(name='reciever', description=CMD_DESC[18], option_type=3, required=True)])
async def _restoreSubmit(ctx:SlashContext, reciever: str): 
    await restoreSubmit(ctx, reciever, client)

client.run(TOKEN)
