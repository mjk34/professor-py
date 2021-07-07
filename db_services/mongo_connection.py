import os
from dotenv import load_dotenv
from pymongo import MongoClient
mongo_connection = None

load_dotenv()
MONGO_CONNECTION_KEY = os.getenv('CONNECTION_KEY')
def getMongo_connection():
    global mongo_connection
    if not mongo_connection:
        mongo_connection = MongoClient(MONGO_CONNECTION_KEY)
    return mongo_connection