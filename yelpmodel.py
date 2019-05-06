# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.
Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""

from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import random

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app

class yelpmodel:
    API_KEY="feIeTg1Me0xHPzBn0IB_MiEbjGCC56SIDkH1y7x6S6GydOiGBYb9KipEU5Vjw_krzkXYM-xekgzNvcHtcJ4VdiwGMs2V9W6Kd00_c9QPpPVK8iIMM5cFYc0MDhrKXHYx" 

    # API constants, you shouldn't have to change these.
    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

    # Defaults for our simple example.
    DEFAULT_TERM = 'dinner'
    DEFAULT_LOCATION = 'San Francisco, CA'
    SEARCH_LIMIT = 50


    def request(self, host, path, api_key, url_params=None):
        """Given your API_KEY, send a GET request to the API.
        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            API_KEY (str): Your API Key.
            url_params (dict): An optional set of query parameters in the request.
        Returns:
            dict: The JSON response from the request.
        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % api_key,
        }

        response = requests.request('GET', url, headers=headers, params=url_params)

        return response.json()


    def search(self, api_key, term, location):
        """Query the Search API by a search term and location.
        Args:
            term (str): The search term passed to the API.
            location (str): The search location passed to the API.
        Returns:
            dict: The JSON response from the request.
        """

        url_params = {
            'location': location.replace(' ', '+'),
            'term': term.replace(' ', '+'),
            'limit': self.SEARCH_LIMIT
        }
        return self.request(self.API_HOST, self.SEARCH_PATH, api_key, url_params=url_params)


    def get_business(self, business_id):
        """Query the Business API by a business ID.
        Args:
            business_id (str): The ID of the business to query.
        Returns:
            dict: The JSON response from the request.
        """
        business_path = self.BUSINESS_PATH + business_id

        return self.request(self.API_HOST, business_path, self.API_KEY)


    def query_api(self, term, location):
        """Queries the API by the input values from the user.
        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        """
        response = self.search(self.API_KEY, term, location)

        businesses = response.get('businesses')

        return businesses


    def findRestaurantByCuisine(self, cuisine):
        """Changed it so that this function returns a random restaurant"""

        restaurantList = self.query_api(cuisine, "Monterey, CA")
        oneRandomRestaurant = random.choice(restaurantList)
        return self.get_business(oneRandomRestaurant['id'])
