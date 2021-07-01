import os
import discord
from dotenv import load_dotenv

from cmd import pong, halp, playlist, mal, anichart

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

    await client.change_presence(activity=discord.Game('>help'))


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
        await mal(message, message_string)

    if 'anichart' in message_string:
        await anichart(message, message_string)
        
client.run(TOKEN)