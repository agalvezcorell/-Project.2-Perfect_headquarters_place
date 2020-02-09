from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
load_dotenv()

def requestFour(codigo,lugar):
    """
    Hace una request a la api de Foursquare si le das un string
    con lo que estás buscando o con la clave de búsqueda de Foursquare
    y un lugar.
    """
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
    

def BuscayExporta(categoria):
    tok1 = os.getenv("CLIENT_ID")
    tok2 = os.getenv("CLIENT_SECRET")
    LAT = 13.40452
    LON = 52.50135
    params = {"client_id": tok1,
  "client_secret":tok2,
  "v":"20180323",
  "ll":f'{LON},{LAT}',
  "query":f'{categoria}',
  "limit":100
}  
    url = 'https://api.foursquare.com/v2/venues/explore'
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    df1 = pd.DataFrame(data)
    loc = df1.iat[10,1]
    df2 = pd.DataFrame(loc)
    df3 = df2.explode('items')
    df3.to_json(f"output/{categoria}", orient="records")
