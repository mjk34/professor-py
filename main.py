import os
import discord
from dotenv import load_dotenv

from cmd import pong, halp, playlist, fetchMSG
from creds import daily, getCreds, clearDatabase
from creds import purchase, give, setBirthday, checkBirthday

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
MESSAGE_TOKEN = '>'

@client.event
async def on_ready():
    
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    await client.change_presence(activity=discord.Game('<help'))
    await checkBirthday(guild, client)


@client.event
async def on_message(message):
    if message.author == client.user: return        # checks if the message sender is not a bot
    if message.author.guild.name != GUILD: return   # checks if it's from UwUversity
    if message.channel.name != "bot-cmd": return    # checks if it comes from the bot channel
    if message.content[0] != MESSAGE_TOKEN:return   # checks if the leading token is correct

    # Get the rest of the message
    message_string = message.content.lower()[1:]

    # List of message commands
    if 'ping' in message_string: 
        await pong(message)

    if 'help' in message_string:
        await halp(message, message_string)

    if 'playlist' in message_string:
        await playlist(message, message_string)

    if 'mal' in message_string:
        await fetchMSG(message, message_string)

    if 'anichart' in message_string:
        await fetchMSG(message, message_string)

    if 'setbd' in message_string:
        await setBirthday(message)

    if 'rewards' in message_string:
        await fetchMSG(message, message_string)  

    if 'bronze' in message_string:
        await purchase(message, message_string)

    if 'silver' in message_string:
        await purchase(message, message_string)

    if 'gold' in message_string:
        await purchase(message, message_string)

    if 'platinum' in message_string:
        await purchase(message, message_string)

    if 'uwu' in message_string:
        await daily (message)

    if 'creds' in message_string:
        await getCreds (message)

    if 'clear' in message_string:
        await clearDatabase (message)

    if 'give' in message_string:
        await give (message, message_string, client)
  
client.run(TOKEN)