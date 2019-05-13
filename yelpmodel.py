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


    def search(self, api_key, term, location, open_now):
        """Query the Search API by a search term and location.
        Args:
            term (str): The search term passed to the API.
            location (str): The search location passed to the API.
            open_now (bool): The search open_now passed to the API 
        Returns:
            dict: The JSON response from the request.
        """

        url_params = {
            'location': location.replace(' ', '+'),
            # 'term': term.replace(' ', '+'),
            'categories': term.lower(),
            'open_now': open_now, 
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


    def query_api(self, term, location, open_now):
        """Queries the API by the input values from the user.
        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        """
        response = self.search(self.API_KEY, term, location, open_now)

        businesses = response.get('businesses')

        return businesses


    ''' 
    def findRestaurantByCuisine(self, cuisine):

        # RestaurantList is a list of all of the Yelp IDs of restaurants in Monterey fitting the cuisine
        restaurantList = self.query_api(cuisine, "Monterey, CA", True)
        oneRestaurant = dict(restaurantList)
        return self.get_business(restaurantList['id'])
    '''
    def findRestaurantByCuisine(self, cuisine):
        # RestaurantList is a list of all of the Yelp IDs of restaurants in Monterey fitting the cuisine
        restaurantList = self.query_api(cuisine, "Monterey, CA", True)
        # Results will be a list of dictionaries of all of the restaurants' information
        results = list()
        # For each restaurant, get a dictionary with all of its information and append it to results
        for restaurant in restaurantList:
            results.append(self.get_business(restaurant['id']))
        return results


    # Gets one random restaurant with the specified cuisine and returns a dictionary of its data
    def getRandomRestaurantByCuisine(self, cuisine):
        # RestaurantList is a list of all of the Yelp IDs of restaurants in Monterey fitting the cuisine
        restaurantList = self.query_api(cuisine, "Monterey, CA", True)
        # Choose a random restaurant
        oneRandomRestaurant = random.choice(restaurantList)
        # Get and return that restaurant's dictionary
        return self.get_business(oneRandomRestaurant['id'])