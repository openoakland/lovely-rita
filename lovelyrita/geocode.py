import time
import requests
import datetime
import pandas as pd
from lovelyrita.config import API_KEY

API_URL = "https://maps.googleapis.com/maps/api/geocode/"

class Geocoder(object):
    def __init__(self, output_path, api_url=API_URL, api_key=API_KEY):
        self.output_path = output_path
        self.geocodes = self.load_geocodes(output_path)
        self.api_url = api_url
        self.api_key = API_KEY

    def load_geocodes(self, path):
        return pd.read_csv(path)

    def geocode(address, pause_time=0.1):
        """
        Pull data from Google Maps API
        """
        # check if query has already been run
        if address in self.geocodes:
            return self.geocodes[address]

        query = {'address': address,
                 'key': self.api_key}
        url = self.api_url + 'json/?' + urlencode(query)
        response = requests.get(url)
        time.sleep(pause_time) # to prevent lockout
        content = response.json()
        if not content:
            return None     
        elif content["status"] != 'OK':
            return query
        else:
            place_id = content['results'][0]['place_id']
            lat = content['results'][0]['geometry']['location']['lat']
            lon = content['results'][0]['geometry']['location']['lon']

            content["timestamp"] = str(datetime.datetime.now())
            return lat, lon, place_id
