import random
import discord
import API.API
import os

from dotenv import load_dotenv
from datetime import date, timedelta, datetime
from dateutil import parser
from discord.utils import get

api = API.API
load_dotenv()
ADMIN = int(os.getenv('ADMIN_ID'))
MODERATOR1 = int(os.getenv('VHCHENG'))

async def getScore(ctx, k, d, a, multi, head, rounds):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_submit = api.fetchSubmit(id)
    if user_submit == 2:
        await ctx.send(
            f'<@{id}>, you are out of submission attempts, try **/uwu** to reset'
        )
        return
    
    kda = (k + a) / d
    game = rounds / 25

    score = int(100*kda*game + 2*head + 30*multi)
    if score > 0:
        message_to_pin = await ctx.send(
            f'KDA {k}/{d}/{a} | MULTI: {multi} | HEAD: {head} | ROUNDS: {rounds}' +
            f'\n<@{id}>, based on the given input, you got a uwuScore of **{score}**'
        )
        await message_to_pin.pin()
        api.incrementSubmit(id)
    else: await ctx.send(f'InPuT pArAmEtErS aRe BaD, pLs TrY aGaIn!1!')

async def getSubmit(ctx):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_submit = api.fetchSubmit(id)
    await ctx.send(
        f'<@{id}>, you are at {user_submit}/2 valorant submissions' +
        f'\nTwo submissions are allowed per day, submission attemps will reset after daily **/uwu**'
    )

async def raffle(ctx):
    id = ctx.author.id
    name = ctx.author.name
    today, yesterday = getTime()

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_tickets = api.fetchTicket(id)
    await ctx.send(
        f'<@{id}>, you have {user_tickets} ticket(s)' +
        f'\nRaffle tickets are used to compete for a free valorant battle pass' +
        f'\nTickets can be bought using **/ticket** with uwuCreds, 2000 + 400n'
    )

async def leaderboard(ctx):
    top_users = api.getTopUsers()
    user_list = 'TOP SERVER\n-----------------------------------------\n'
    count = 1
    for user in top_users:
        user_list += f'** #{count} ** {user[0]:-<20}  ({user[1]}/{user[2]})\n'
        count += 1

    await ctx.send(user_list)

def getTime():
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    today = today.strftime('%m-%d-%y %H:%M')
    yesterday = yesterday.strftime('%m-%d-%y %H:%M')

    return today, yesterday
