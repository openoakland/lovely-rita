import re
import requests
import datetime
from urllib.parse import urlencode
import psycopg2
import pandas as pd
from lovelyrita.config import API_KEY


API_URL = "https://maps.googleapis.com/maps/api/geocode/"


class Geocoder(object):
    def __init__(self, geocodes=None, api_url=API_URL, api_key=API_KEY):
        if geocodes is None:
            geocodes = pd.DataFrame(columns=('lat', 'lng', 'place_id', 'timestamp'))
            geocodes.index.name = 'address'
        self.geocodes = geocodes
        self.api_url = API_URL
        self.api_key = API_KEY

    def geocode(self, address):
        """
        Pull data from Google Maps API

        Parameters
        ----------
        address : str
        """
        # check if query has already been run
        try:
            g = self.geocodes.loc[address]
            return g['lat'], g['lng'], g['place_id']
        except KeyError:
            pass

        query = {'address': address,
                 'key': self.api_key}
        url = self.api_url + 'json?' + urlencode(query)
        response = requests.get(url)
        if response.status_code == 404:
            raise Exception("404 error for {}".format(url))

        content = response.json()
        if content['status'] != 'OK':
            raise Exception("Status not OK for {}".format(url))

        place_id = content['results'][0]['place_id']
        lat = content['results'][0]['geometry']['location']['lat']
        lng = content['results'][0]['geometry']['location']['lng']
        timestamp = str(datetime.datetime.now())

        new_geocode = pd.Series({'place_id': place_id,
                                 'lat': lat, 'lng': lng,
                                 'timestamp': timestamp},
                                name=address)
        self.geocodes = self.geocodes.append(new_geocode)
        return lat, lng, place_id

    @classmethod
    def load(cls, geocode_path):
        return cls(load_geocodes(geocode_path))

    def save(self, geocode_path):
        save_geocodes(self.geocodes, geocode_path)


class PostGISGeocoder(object):
    def __init__(self, host='172.17.0.3', database='postgres', user='postgres',
                 password='mysecretpassword'):
        """A PostGIS geocoder
        """
        connection = psycopg2.connect(host=host, database=database,
                                      user=user, password=password)
        self.connection = connection
        self.cursor = connection.cursor()

    def geocode(self, address):
        """Get the latitude and longitude of an address

        Parameters
        ----------
        address : str

        Returns
        -------
        A dictionary containing keys latitude, longitude, street_number, street_name, street_type, and 
        rating (a numeric value indicating how uncertain the geocoding is)
        """
        patt = "[" + re.escape("()\'+") + "]"
        address = re.sub(patt, '', address)

        columns = ['rating', 'longitude', 'latitude',
                   'street_number', 'street_name', 'street_suffix']

        query = ("""SELECT g.rating, ST_X(g.geomout) As lon, ST_Y(g.geomout) As lat, """
                 """(addy).address As stno, (addy).streetname As street, """
                 """(addy).streettypeabbrev As styp, """
                 """(addy).location As city, """
                 """(addy).stateabbrev As st,(addy).zip """
                 """FROM geocode(%s, 1) As g;""")
        self.cursor.execute(query, (address, ))
        response = self.cursor.fetchone()

        if response:
            result = {k: v for k, v in zip(columns, response)}
        else:
            result = [None, ] * len(columns)

        return result


def geocode_citations(citations, rating=10, geocoder=None):
    """Geocode a DataFrame of citations
    
    Parameters:
    -----------
    citations : pandas DataFrame
    rating : int
    
    Returns:
    --------
    A DataFrame with geocoded latitude and longitude
    """
    if 'latitude' not in citations.columns:
        citations['latitude'] = np.nan
    if 'longitude' not in citations.columns:
        citations['longitude'] = np.nan

    if geocoder is None:
        geocoder = PostGISGeocoder()

    results = []
    indices = []
    for index, row in citations.iterrows():
        res = geocoder.geocode(row['street'] + ', oakland, ca')
        if res['rating'] < rating:
            indices.append(index)
            results.append(res)
        else:
            print(res)

    results = pd.DataFrame(results, index=indices)
    citations.update(results)

    return citations
