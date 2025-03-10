import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv() 

# Define the API endpoint for token generation
token_url = "https://api.myuplink.com/oauth/token"

# Define the payload for the token request
payload = {
    "client_id": "27a85d09-2380-437e-83a4-f7f4e7f13b98",
    "client_secret": os.getenv("CLIENT_SECRET"),
    "grant_type": "client_credentials",
    "scope": "READSYSTEM WRITESYSTEM"
}

# Define the headers for the request
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Make the POST request to generate the token
response = requests.post(token_url, data=payload, headers=headers)
token = response.json().get("access_token")

import requests

# Define the API endpoint
url = "https://api.myuplink.com/v2/devices/emmy-r-29350-20240309-06603616062027-d8-80-39-87-32-f9/points"

from pymongo import MongoClient
from time import sleep

client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']

while True:
    db_timestamp = datetime.now().isoformat()

    try:

        # Make the GET request
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        data = response.json()

        for item in data:
            item['db_timestamp'] = db_timestamp
            collection.insert_one(item)
            
        print(f"Inserted {len(data)} items into the database at {db_timestamp}")

    except Exception as e:
        print(f"An error occurred: {e}")

    sleep(60*10)
