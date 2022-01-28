# import os

# from dotenv import load_dotenv
# from datetime import date, timedelta, datetime
# from dateutil import parser
# from discord.utils import get

# from helper1 import getTime, getAverage, getWeight

# api = API.API
# load_dotenv()
# ADMIN = int(os.getenv('ADMIN_ID'))
# MODERATOR1 = int(os.getenv('VHCHENG'))

# filler = ['<', '>', '!', '@']

# async def getScore(ctx, k, d, a, adr, head, rounds, submit):
#     """user can view or submit a valorant match to earn uwuCreds,
#        uwuscore is based on kills, deaths, assists, adr, headshot,
#        and total rounds. The calculated score is then scaled based
#        on user average score of past 10 game scores
#     """
#     id, name = ctx.author.id, ctx.author.name
#     yesterday = getTime(True)
#     user = api.fetchUser(id)
#     if len(user) == 0: api.createAccount(id, name, yesterday)

#     """check if the user has submissions left"""
#     user_submit = api.fetchSubmit(id)
#     if user_submit == 3:
#         await ctx.send(
#             f'<@{id}>, you are out of submission attempts, try **/uwu** to reset'
#         )
#         return
    
#     """calculate uwuScore, check for divide by zero"""
#     if d <= 4: d = 4 # prevent scaling above 800
#     kda, game = (k + 0.5*a) / d, rounds / 25  
#     score = int(kda*game*(adr + 3*head))
    
#     """fetch and calculate user average/score weight"""
#     history = api.fetchValHistory(id)
#     print(history)
#     final_score = 0
#     if len(history) > 3:
#         average = getAverage(history)
#         print(average)
#         weight = getWeight(average, score)
#         print(weight)
        
#         if score > average: final_score = int(score + 0.666*score*weight)
#         else: final_score = int(score - 1.5*score*weight)
        
#     else:
#         final_score = score
    
#     if final_score > 0:
#         message_to_pin = await ctx.send(
#             f'KDA {k}/{d}/{a} | ADR: {adr} | HEAD: {head} | ROUNDS: {rounds}' +
#             f' ---> uwuScore of **{final_score}**'
#         )
        
#         """if submit, update uwuDB, append new final score"""
#         if submit:
#             await message_to_pin.pin()
#             api.incrementSubmit(id)
            
#             if len(history) >= 10: history.pop(0)
#             history.append(final_score)
#             api.updateValHistory(id, history)    
                     
#     else: await ctx.send(f'InPuT pArAmEtErS aRe BaD, pLs TrY aGaIn!1!')