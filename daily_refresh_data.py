from pymongo import MongoClient
from random import randint
from urllib.request import urlopen
import requests
from requests.exceptions import HTTPError
#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient('mongodb+srv://kunwar:kunwar$123@cluster0.z3w9w.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=client.Covid

try:
    response = requests.get('https://covidtracking.com/api/us/daily')
    response.raise_for_status()
    db.stats.drop()
    jsonResponse = response.json()
    db.stats.insert_many(jsonResponse)
    print('Data Refresh Completed!')

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
