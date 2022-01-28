# import random
# from datetime import timedelta, datetime
# from typing import Iterable, List, Union
# from dateutil import parser

# def replaceList (list_of_strings:list, old:str, new:str) -> list:
#     """replaces a character throught a list of strings"""
#     for i in range(len(list_of_strings)):
#         list_of_strings[i] = list_of_strings[i].replace(old, new)
#     return list_of_strings

# def getTime (yesterday:bool) -> str:
#     """fetches either todays or yesterdays date and time"""
#     time = datetime.now()
#     if yesterday: time = time - timedelta(days=1)
#     return time.strftime('%m-%d-%y %H:%M')  

# def timeDiff (time1 :str, time2:str):
#     """finds the difference in time between time1 and time2"""
#     time1 = parser.parse(time1)
#     time2 = parser.parse(time2)
#     return time2 - time1

# def lessThan24HRs (time_diff) -> bool:
#     """checks if time difference is less than a day"""
#     return {True:True, False:False}[time_diff < timedelta(hours=20)]

# def timeWait (time_diff):
#     """finds the wait time till next daily"""
#     return timedelta(hours=20) - time_diff
    
# def fetchCMD () -> list:
#     """fetches a list of slash command descriptions"""
#     command_lines = []
#     with open('./messages/command.txt', 'r') as file:
#         command_lines = file.readlines()
#     return replaceList(command_lines, '\n', '')

# def dailyLuck () -> Iterable[Union[int, str]]:
#     """randomly generates a number from 1 to 10001 and
#        produce credits and status description based on 
#        probability range it falls into"""
#     luck = random.randint(1, 1001)
#     cred_amount, cred_status = 0, ''

#     if luck <= 550: 
#         cred_amount = random.randint(100, 250)
#         cred_status = '*oof...*'
#     if luck > 550 and luck <= 850: 
#         cred_amount = random.randint(300, 500)
#         cred_status = 'Ok, not bad,'
#     if luck > 850 and luck <= 950: 
#         cred_amount = random.randint(600, 700)
#         cred_status = '**Super Pog**,'
#     if luck > 950 and luck <= 1000:
#         cred_amount = random.randint(800, 900)
#         cred_status = '***Kyaaaaaaa!!***,'
#     if luck == 1001:
#         cred_amount = 5000
#         cred_status = 'RNJesus has blessed you, '
#     return cred_amount, cred_status

# def rewardCost (tier:str, num_tickets:int) -> int:
#     """return cost depending on tier string, for the ticket
#        tier- scale cost on the number of tickets already obtained

#     Args:
#         tier (str): [reward levels shown in /help]
#         num_tickets (int): [existing ticket in userDB]

#     Returns:
#         int: [the total cost of the purchase]
#     """
#     cred_cost = 0
#     if tier == 'ticket':    cred_cost = 2000 + 400*(num_tickets)
#     return cred_cost

# def getAverage(history):
#     sum = 0
#     for i in range(len(history)):
#         sum += history[i]
#     return int(sum/len(history))

# def getWeight(average, score):
#     return (average - score) / (average + score)