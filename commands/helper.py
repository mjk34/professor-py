import random, requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from typing import Iterable, Union
from dateutil import parser
from pytz import timezone

est = timezone('EST')
cst = timezone('US/Central')

"""Replaces a character in all string of a list"""
def replaceList (list_of_strings:list, old:str, new:str) -> list:
    for i in range(len(list_of_strings)):
        list_of_strings[i] = list_of_strings[i].replace(old, new)
    return list_of_strings

"""Fetches each line of a text file in a list"""
def fetchContentList (filename) -> list:
    lines = []
    with open(f'./messages/{filename}', 'r') as file:
        lines = file.readlines()
    return replaceList(lines, '\n', '')

"""Fetches the contents of a text file"""
def fetchContent (filename) -> str:
    filename = f'./messages/{filename}'
    f = open(filename, 'r')
    return f.read(), f

"""Fetches today's date"""
def todayTime () -> str:
    time = datetime.now(cst)
    return str(time.strftime('%m-%d-%y %H:%M:%S'))

"""Fetches today's date in depth"""
def today () -> str:
    time = datetime.now(est)
    return str(time.strftime('%m-%d-%y'))

"""Fetches the current monday"""
def thisMonday () -> str:
    today = datetime.now(est)
    weekday =  datetime.weekday(today)

    if weekday == 0: return str(today.strftime('%m-%d-%y'))
    else: 
        monday = today + timedelta(days=-weekday)
        return str(monday.strftime('%m-%d-%y'))

"""Checks if the designated monday is the current monday"""
def checkMonday (block_date) -> bool:
    block_datetime = parser.parse(block_date)
    block_week = datetime.weekday(block_datetime)
    block_monday = ''

    if block_week == 0: 
        block_monday = str(block_datetime.strftime('%m-%d-%y'))
    else:
        temp_monday = block_datetime + timedelta(days=-block_week)
        block_monday = str(temp_monday.strftime('%m-%d-%y'))

    if block_monday == thisMonday(): return True
    return False


"""Randomly generate luck based on values 1-1001"""
def dailyLuck (server_bonus) -> Iterable[Union[int, str]]:
    luck = random.randint(1, 956)
    multiplier = [0, 1.25, 1.50, 1.75, 2.0]
    cred_amount, cred_status = 0, ''

    if luck <= 300: 
        cred_amount = random.randint(100, 250)
        cred_status = '*Congrats, you are cursed*.'
    if luck > 300 and luck <= 550: 
        cred_amount = random.randint(250, 400)
        cred_status = '*A honest sum, nothing more*.'
    if luck > 550 and luck <= 750: 
        cred_amount = random.randint(400, 500)
        cred_status = '**Fortune favors you**,'
    if luck > 750 and luck <= 920:
        cred_amount = random.randint(500, 700)
        cred_status = '***The currents of Causality bends for you***,'
    if luck > 925:
        cred_amount = 2000
        cred_status = 'You  are  the  **biggest**  *bird*.'

    if int(server_bonus/3) == 1: cred_amount *= 1.25
    if int(server_bonus/3) == 2: cred_amount *= 1.50
    if int(server_bonus/3) == 3: cred_amount *= 1.75
    if int(server_bonus/3) >= 4: cred_amount *= 2.00
    
    return int(cred_amount), cred_status

"""Randomly generate fortune readings from fortune-api"""
def dailyFortune () -> str:
    response = requests.get('https://fungenerators.com/random/fortune-cookie/')
    soup = BeautifulSoup(response.content, 'html.parser')
    contents = soup.find('h2').get_text()

    return str('\"' + contents + '\"')

"""Fetch difference between the average and score"""
def getWeight(average, score) -> float:
    return abs(float((average - score) / (average + score)))

"""Fetch discord user's Name by Id"""
async def getName(id, client) -> str:
    user_object = await client.fetch_user(id)
    return str(user_object.name)
    
"""Fectch discord user's Icon by Id"""
async def getIcon(id, client) -> str:
    user_object = await client.fetch_user(id)
    return str(user_object.avatar_url)

if __name__ == '__main__':
    print(checkMonday('9-13-2022'))
    print(checkMonday('9-12-2022'))