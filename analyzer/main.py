from fastapi import FastAPI
from typing import List
from pymongo import MongoClient
from starlette.responses import StreamingResponse
import os
import io
from bson.objectid import ObjectId
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


@app.get('/person', response_model=List[Person])
async def root():
    client = get_client()
    db = client["mydatabase"]
    col = db["people"]
    return list(col.find({}, {"photo": 0}))


@app.get("/person/{item_id}", response_model=Person)
async def read_item(item_id):
    obj_id = ObjectId(item_id)
    client = get_client()
    db = client["mydatabase"]
    col = db["people"]
    person = col.find_one(obj_id, {"photo": 0})
    return person


@app.get("/person/{item_id}/photo")
async def read_item(item_id):
    obj_id = ObjectId(item_id)
    client = get_client()
    db = client["mydatabase"]
    col = db["people"]
    file_bytes = col.find_one(obj_id)['photo']
    return StreamingResponse(io.BytesIO(file_bytes), media_type="image/png")