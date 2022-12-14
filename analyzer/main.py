from fastapi import FastAPI
from typing import List
from pymongo import MongoClient
import os
from urllib.parse import quote_plus

from models.person import Person

app = FastAPI()


def get_client():
    host = os.getenv('MONGODB_HOST', '')
    username = os.getenv('MONGODB_USER', '')
    password = os.getenv('MONGODB_PASSWORD', '')
    port = int(os.getenv('MONGODB_PORT', 27017))
    endpoint = 'mongodb://{0}:{1}@{2}'.format(quote_plus(username), quote_plus(password), host)
    mongo_client = MongoClient(endpoint, port)
    return mongo_client


@app.get('/', response_model=List[Person])
async def root():
    client = get_client()
    db = client["mydatabase"]
    col = db["people"]
    return list(col.find({}))
