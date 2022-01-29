import block, blockchain
from helper import today
from datetime import timedelta, datetime
from dateutil import parser

"""Evaluated Blockchain:
        1. find the most recent daily based on user_id
        2. check if the date difference is greater than 0"""
def hasDaily(user_id, BLOCKCHAIN) -> bool: 
    desc, date = 'Daily', ''
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                date = block.getTime()
                     
    if date == '': return True
    time_diff = parser.parse(today()) - parser.parse(date)
    return {True:False, False:True}[time_diff == timedelta(seconds=0)]

"""Evaluate Blockchain:
        1. run through each block belonging to user_id
        2. for each block, add up all data transactions"""
def totalCreds(user_id, BLOCKCHAIN) -> int:
    total = 0
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            total += block.getData()
    
    return total