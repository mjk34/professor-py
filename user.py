import block, blockchain
from helper import today
from datetime import timedelta, datetime
from dateutil import parser

def hasDaily(user_id, BLOCKCHAIN) -> bool:
    desc, date = 'Daily', ''
    for block in BLOCKCHAIN.chain[1:]:
        if block.getUser() == user_id:
            if block.getDesc() == desc:
                date = block.getTime()
                     
    time_diff = parser.parse(today()) - parser.parse(date)
    return {True:False, False:True}[time_diff == timedelta(seconds=0)]