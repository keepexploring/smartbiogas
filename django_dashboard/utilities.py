import what3words
from os import environ

api_key='R35K949K' # API key for what3words 

def find_coordinates(address):
    try:
        w3w = what3words.Geocoder(api_key)
        res = w3w.forward(addr=address)
        return res['geometry']
    except:
        return None

def reverse_geocode(lat, long):
    try:
        w3w = what3words.Geocoder(api_key)
        res = w3w.reverse(lat=lat, lng=long)
        return res['words']
    except:
        return None