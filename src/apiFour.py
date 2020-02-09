from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()

def requestFour(codigo,lugar):
    tok1 = os.getenv("CLIENT_ID")
    tok2 = os.getenv("CLIENT_SECRET")
    LAT = lugar.get("coordinates")[0]
    LON = lugar.get("coordinates")[1]
    params = {"client_id": tok1,
  "client_secret":tok2,
  "v":"20180323",
  "ll":f'{LON},{LAT}',
  "query":f'{codigo}',
  "limit":100
}  
    url = 'https://api.foursquare.com/v2/venues/explore'
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data


def requestCateg():
    tok1 = os.getenv("CLIENT_ID")
    tok2 = os.getenv("CLIENT_SECRET")
    url = 'https://api.foursquare.com/v2/venues/categories'
    params = {"client_id": tok1,
  "client_secret":tok2,
    }
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data
    

