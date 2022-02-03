import random, requests, json
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
    luck = random.randint(1, 1011)
    cred_amount, cred_status = 0, ''

    if luck <= 550: 
        cred_amount = random.randint(100, 250)
        cred_status = '*oof...*'
    if luck > 550 and luck <= 850: 
        cred_amount = random.randint(300, 500)
        cred_status = 'Ok, not bad,'
    if luck > 850 and luck <= 950: 
        cred_amount = random.randint(600, 700)
        cred_status = '**Super Pog**,'
    if luck > 950 and luck <= 1000:
        cred_amount = random.randint(800, 900)
        cred_status = '***Kyaaaaaaa!!***,'
    if luck > 1000:
        cred_amount = 2000
        cred_status = 'RNJesus has blessed you, '
    return cred_amount, cred_status

"""Randomly generate fortune readings from fortune-api"""
def dailyFortune () -> str:
    while True:
        response = requests.get('https://fortuneapi.herokuapp.com/')
        response_size = len(response.content)
        if response_size < 200 and response_size > 1: break
        
        
    reading = ''
    reading += str(json.loads(response.text))
    return reading

"""Fetch difference between the average and score"""
def getWeight(average, score) -> float:
    return float((average - score) / (average + score))

"""Fetch discord user's Name by Id"""
async def getName(id, client) -> str:
    user_object = await client.fetch_user(id)
    return str(user_object.name)
    