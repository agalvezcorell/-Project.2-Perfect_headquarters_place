import math
import requests
from geopandas import GeoDataFrame
from shapely.geometry import Point
import pandas as pd
from pymongo import MongoClient
client = MongoClient("mongodb://localhost/companies") 
db = client.get_database()

def asGeoJSON(lat,lng):
    """
    Esta función se asegura de que no haya valores NaN y, aplicada con una lambda
    a dos columnas del DataFrame donde tenemos latitud y longitud, devuelve un
    diccionario con el formato de MongoDB para guardar coordenadas y poder hacer
    indexes
    """
    try:
        lat = float(lat)
        lng = float(lng)
        if not math.isnan(lat) and not math.isnan(lng):
            return {
                "type":"Point",
                "coordinates":[lng,lat]
            }
    except Exception:
        print("Invalid data")
        return None


def geocode(address):
    """
    Saca las coordenadas de una dirección que le des.
    """
    data = requests.get(f"https://geocode.xyz/{address}?json=1").json()
    return {
        "type":"Point",
        "coordinates":[float(data["longt"]),float(data["latt"])]}


def withGeoQuery(location,maxDistance=2000,minDistance=0,field="location"):
    """
    Devuelve un diccionario para poder hacer una query a MongoDB y ver si en
    el punto que le ponga hay empresas de más de 9 años en 2km
    """
    return {
       field: {
         "$near": {
           "$geometry": location if type(location)==dict else geocode(location),
           "$maxDistance": maxDistance,
           "$minDistance": minDistance
         }
       }
    }


def VisualizaCarto(df):
    """
    Esta función convierte un df en un geodataframe
    """
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    crs = {'init': 'epsg:4326'}
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
    return gdf


def aDataF(lugar):
    """
    Esta función convierte un elemento que tenga latitud y longitud
    en un geodataframe para poder visualizarlo en Cartoframes.
    """
    data = [{ "latitude": lugar[1],
    "longitude":lugar[0]
    }]
    df = pd.DataFrame(data)
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    crs = {'init': 'epsg:4326'}
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
    return gdf

def GoodList(lista):
    goodlist = []
    for a in lista:
        for b in a.values():
            for c in b.values():
                goodlist.append(c)
    
    return goodlist


def GeoDataframe(lista):
    df_lista = pd.DataFrame(lista)
    dfotro = df_lista[["location"]].apply(lambda r: r.location, result_type="expand", axis=1)
    dfcoord = dfotro[["lat","lng"]].rename(columns={"lat": "latitude", "lng":"longitude"})
    lista_map = VisualizaCarto(dfcoord)
    lista_map["name"] = df_lista["name"]
    return lista_map
"""
def findNear(list_geo, radio_meters,col):

        geopoint = list_geo
        return list(db.starbien.find({
        "location": {
         "$near": {
             "$geometry": geopoint,
             "$maxDistance": radio_meters
         }
    }
    }
    )
    )
    """