import random, requests, json
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from typing import Iterable, Union
from dateutil import parser
from pytz import timezone

est = timezone('EST')

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
def today () -> str:
    time = datetime.now(est)
    return str(time.strftime('%m-%d-%y'))

"""Randomly generate luck based on values 1-1001"""
def dailyLuck () -> Iterable[Union[int, str]]:
    luck = random.randint(1, 1006)
    cred_amount, cred_status = 0, ''

    if luck <= 450: 
        cred_amount = random.randint(100, 200)
        cred_status = '*Yikers bruv, this aint it.*'
    if luck > 450 and luck <= 750: 
        cred_amount = random.randint(200, 400)
        cred_status = '*Another day, another stack of creds*.'
    if luck > 750 and luck <= 950: 
        cred_amount = random.randint(400, 500)
        cred_status = '**Ara Ara! Super Pog**,'
    if luck > 950 and luck <= 1000:
        cred_amount = random.randint(500, 700)
        cred_status = '***Kyaaaaaaa!!***,'
    if luck > 1000:
        cred_amount = 2000
        cred_status = 'RNJesus has blessed you, '
    return cred_amount, cred_status

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