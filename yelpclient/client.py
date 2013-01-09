#!/usr/bin/env python
#
# Copyright 2012 Johnie Lee
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

'''
Yelp API Client implementation.

Python client implementation for the Yelp API
(http://www.yelp.com/developers/documentation/v2/search_api)
'''

from urllib import urlencode

import logging
import oauth2
import requests
import time

logger = logging.getLogger(__name__)

class YelpClient(object):
    '''
        Yelp Api Client implementation
        See: http://www.yelp.com/developers/documentation/v2/search_api
    '''

    class SortType:
        '''Enum representing the sort options for search results'''
        BEST_MATCHED, DISTANCE, HIGHEST_RATED = range(3)

    _yelp_api_root = 'http://api.yelp.com'
    _search_api_path = _yelp_api_root + '/v2/search?'
    _business_api_path = _yelp_api_root + '/v2/business?'

    def __init__(self, yelp_keys):
        logger.info('Initializing YelpClient with %s'
                    % yelp_keys['consumer_key'])
        self.__consumer_key = oauth2.Consumer(yelp_keys['consumer_key'],
                                              yelp_keys['consumer_secret'])
        self.__token = oauth2.Token(yelp_keys['token'],
                                    yelp_keys['token_secret'])

    def _sign_request(self, url):
        logger.debug('Signing request for %s' % url)
        params = {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_token': self.__token.key,
            'oauth_consumer_key': self.__consumer_key.key,
        }

        request = oauth2.Request('GET', url, params)
        request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(),
                             self.__consumer_key, self.__token)
        return request.to_url()

    def _search(self, **kwargs):
        filtered_query_map = dict((k, v) for k, v in kwargs.iteritems()
                                  if v is not None)

        signed_url = self._sign_request(YelpClient._search_api_path
                                        + urlencode(filtered_query_map))
        logger.debug('Signed url: %s' % signed_url)
        result = requests.get(signed_url)
        logger.debug('Executed request')
        return result.json()

    def search_by_location(self, location, term=None, limit=None, offset=None,
                           sort=None, category=None, radius=None):
        '''Search by Location.

            Params:
                location : combination of "address, neighborhood, city,
                    state or zip, optional country" to be used when searching
                    for businesses.
                term     : term to search for
                limit    : number of results to return
                offset   : offset for the first result
                sort     : Sort type.  Use the SortType enum
        '''

        if location is None:
            raise ValueError("location is required.")

        logger.debug('Searching for %s in %s' % (term, location))

        query_map = {
            'location': location,
            'term': term,
            'limit': limit,
            'offset': offset,
            'sort': sort,
            'category': category,
            'radius': radius,
        }

        return self._search(**query_map)

    def search_by_geo_coord(self, latlong, term=None, limit=None, offset=None,
                            sort=None, category=None, radius=None):
        '''Search by Location.

            Params:
                latlong  : Latitude/Longitude as tuple (float, float) [req'd]
                term     : term to search for
                limit    : number of results to return
                offset   : offset for the first result
                sort     : Sort type.  Use the SortType enum
        '''

        if latlong is None or len(latlong) != 2:
            raise ValueError("latlong is required.")

        logger.debug('Searching for %s in %s' % (term, latlong))

        query_map = {
            'll': ','.join(map(str, latlong)),
            'term': term,
            'limit': limit,
            'offset': offset,
            'sort': sort,
            'category': category,
            'radius': radius,
        }

        return self._search(**query_map)
