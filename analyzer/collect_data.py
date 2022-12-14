import io
import os
import urllib.request
from collections import defaultdict
from typing import Dict

import pandas as pd
import requests
from PIL import Image
from requests import Response

from models.person import Person
from main import get_client


def create_person(person: Person) -> None:
    client = get_client()
    db = client["mydatabase"]
    col = db["people"]
    col.insert_one(person.dict())


def analyze_photo(photo_url: str = os.getenv('PHOTO_ANALYZER_URL', '')) -> Response:
    url = photo_url
    querystring = {"url": os.getenv('PHOTO_URL', '')}
    headers = {
        "X-RapidAPI-Key": os.getenv('API_KEY', ''),
        "X-RapidAPI-Host": os.getenv('API_HOST', '')
    }
    return requests.request("GET", url, headers=headers, params=querystring)


def get_response(side: str) -> Dict:
    response = requests.get(side)
    if response.ok:
        return response.json()
    return defaultdict(str)


def save_photo(photo_url: str = os.getenv('PHOTO_ANALYZER_URL', '')) -> bytes:
    urllib.request.urlretrieve(photo_url, 'tomek.jpg')
    im = Image.open('tomek.jpg')
    image_bytes = io.BytesIO()
    im.save(image_bytes, format='JPEG')
    return image_bytes.getvalue()


def find_data() -> None:
    people_data = pd.read_csv("babynames-clean.csv")
    name, gender = people_data.sample()
    gender = get_response(os.getenv('GENDERIZE_URL', '') + name)['gender']
    age = get_response(os.getenv('AGIFY_URL', '') + name)['age']
    countries = get_response(os.getenv('NATIONALIZE_URL', '') + name)['country']
    country = max(countries, key=lambda c: c['probability'])
    face_response = analyze_photo()
    face_data = {} if face_response.ok else face_response.json()
    photo_data = save_photo()
    person = Person(name=name, gender=gender, age=age, country=country['country_id'], face=face_data, photo=photo_data)
    create_person(person)


if __name__ == "__main__":
    find_data()
