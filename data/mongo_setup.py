import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
CLIENT_URL = os.getenv('CLIENT_KEY')
def global_init():
    client = MongoClient(CLIENT_URL)
    db = client.users
    return db