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
    SEARCH_LIMIT = 3


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

        print(u'Querying {0} ...'.format(url))

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
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': self.SEARCH_LIMIT
        }
        return self.request(self.API_HOST, self.SEARCH_PATH, api_key, url_params=url_params)


    def get_business(self, api_key, business_id):
        """Query the Business API by a business ID.
        Args:
            business_id (str): The ID of the business to query.
        Returns:
            dict: The JSON response from the request.
        """
        business_path = self.BUSINESS_PATH + business_id

        return self.request(self.API_HOST, business_path, api_key)


    def query_api(self, term, location):
        """Queries the API by the input values from the user.
        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        """
        response = self.search(self.API_KEY, term, location)

        businesses = response.get('businesses')

        if not businesses:
            print(u'No businesses for {0} in {1} found.'.format(term, location))
            return

        business_id = businesses[0]['id']

        print(u'{0} businesses found, querying business info ' \
            'for the top result "{1}" ...'.format(
                len(businesses), business_id))
        response = self.get_business(self.API_KEY, business_id)

        print(u'Result for business "{0}" found:'.format(business_id))
        pprint.pprint(response, indent=2)


    def main(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-q', '--term', dest='term', default=self.DEFAULT_TERM,
                            type=str, help='Search term (default: %(default)s)')
        parser.add_argument('-l', '--location', dest='location',
                            default=self.DEFAULT_LOCATION, type=str,
                            help='Search location (default: %(default)s)')

        input_values = parser.parse_args()

        try:
            self.query_api(input_values.term, input_values.location)
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )


# model = yelpmodel()
# model.main()