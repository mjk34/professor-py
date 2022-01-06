import random
import discord
import API.API
import os

from dotenv import load_dotenv
from datetime import date, timedelta, datetime
from dateutil import parser
from discord.utils import get

from helper import getTime, getAverage, getWeight

api = API.API
load_dotenv()
ADMIN = int(os.getenv('ADMIN_ID'))
MODERATOR1 = int(os.getenv('VHCHENG'))

filler = ['<', '>', '!', '@']

async def getScore(ctx, k, d, a, adr, head, rounds, submit):
    """user can view or submit a valorant match to earn uwuCreds,
       uwuscore is based on kills, deaths, assists, adr, headshot,
       and total rounds. The calculated score is then scaled based
       on user average score of past 10 game scores
    """
    id, name = ctx.author.id, ctx.author.name
    yesterday = getTime(True)
    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    """check if the user has submissions left"""
    user_submit = api.fetchSubmit(id)
    if user_submit == 3:
        await ctx.send(
            f'<@{id}>, you are out of submission attempts, try **/uwu** to reset'
        )
        return
    
    """calculate uwuScore, check for divide by zero"""
    if d <= 4: d = 4 # prevent scaling above 800
    kda, game = (k + 0.5*a) / d, rounds / 25  
    score = int(kda*game*(adr + 3*head))
    
    """fetch and calculate user average/score weight"""
    history = api.fetchValHistory(id)
    print(history)
    final_score = 0
    if len(history) > 3:
        average = getAverage(history)
        print(average)
        weight = getWeight(average, score)
        print(weight)
        
        if score > average: final_score = int(score + 0.666*score*weight)
        else: final_score = int(score - 1.5*score*weight)
        
    else:
        final_score = score
    
    if final_score > 0:
        message_to_pin = await ctx.send(
            f'KDA {k}/{d}/{a} | ADR: {adr} | HEAD: {head} | ROUNDS: {rounds}' +
            f' ---> uwuScore of **{final_score}**'
        )
        
        """if submit, update uwuDB, append new final score"""
        if submit:
            await message_to_pin.pin()
            api.incrementSubmit(id)
            
            if len(history) >= 10: history.pop(0)
            history.append(final_score)
            api.updateValHistory(id, history)    
                     
    else: await ctx.send(f'InPuT pArAmEtErS aRe BaD, pLs TrY aGaIn!1!')

async def getSubmit(ctx):
    id = ctx.author.id
    name = ctx.author.name
    yesterday = getTime(True)

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_submit = api.fetchSubmit(id)
    await ctx.send(
        f'<@{id}>, you are at {user_submit}/3 valorant submissions' +
        f'\nTwo submissions are allowed per day, submission attemps will reset after daily **/uwu**'
    )

async def raffle(ctx):
    id = ctx.author.id
    name = ctx.author.name
    yesterday = getTime(True)

    user = api.fetchUser(id)
    if len(user) == 0: api.createAccount(id, name, yesterday)

    user_tickets = api.fetchTicket(id)
    cost = 2000 + 400*(int(user_tickets))
    await ctx.send(
        f'<@{id}>, you have {user_tickets} ticket(s)' +
        f'\nRaffle tickets are used to compete for a free valorant battle pass' +
        f'\nTickets can be bought using **/ticket** with uwuCreds, your next ticket costs: {cost}'
    )

async def leaderboard(ctx):
    top_users = api.getTopUsers()
    user_list = 'TOP SERVER\n-----------------------------------------\n'
    count = 1
    for user in top_users:
        user_list += f'** #{count} ** {user[0]:-<20}  ({user[1]}/{user[2]})\n'
        count += 1

    await ctx.send(user_list)
    
async def restoreSubmit(ctx, reciever, client):
    """allow a moderator user to give back 1 submission to a 
       normal user
    """
    yesterday = getTime(True)
    
    """parse the reciever id from discord <@id> format"""
    giver_id, receive_id = ctx.author.id, reciever
    for ch in filler: receive_id = receive_id.replace(ch, '')
    receive_id = int(receive_id)

    """check if the user exists in uwuDB"""
    giver_db = api.fetchUser(giver_id)
    giver_name = ctx.author.name
    if len(giver_db) == 0: 
        api.createAccount(giver_id, giver_name, yesterday)
        await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')
        return 

    """check if the user is a moderator"""
    role = get(ctx.guild.roles, name='Moderator')
    if role.id in [y.id for y in ctx.author.roles]:
        
        """check if the reciever exists in uwuDB"""
        receive_db = api.fetchUser(receive_id)
        if len(receive_db) == 0:
            receive_object = await client.fetch_user(receive_id)
            receive_name = receive_object.name
            api.createAccount(receive_id, receive_name, yesterday)
        
        """update uwuDB"""
        api.decrementSubmit(receive_id)
        await ctx.send(f'Moderator <@{giver_id}> has restored 1 uwuSubmit to <@{receive_id}>!')
    else: await ctx.send(f'YoU aRe NoT pOwErFuL eNoUgH1!1!')