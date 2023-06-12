import openai
import discord, block, blockchain, random, os

from dotenv import load_dotenv

load_dotenv()
GPT_KEY = os.getenv('API_KEY')
PROFESSOR = int(os.getenv('PROFESSOR_ID'))
ADMIN = int(os.getenv('ADMIN_ID'))

openai.api_key = GPT_KEY

async def gpt_string(context, prompt):
    if random.random() < 0.8:
        uwu_prompt = prompt + f' (make it simple and answer in a cute tone with uwu emojis like a tsundere)'
    else: uwu_prompt = prompt + f' (make it simple and answer in a cute tone with murderous emojis like a yandere)'

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": context},
                {"role": 'user', "content": uwu_prompt}
            ]
        )
    except: 
        return "yo mama"

    return response.choices[0].message.content.strip()