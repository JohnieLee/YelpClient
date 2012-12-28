#!/usr/bin/env python
'''
  Simple CLI for the YelpClient library.
  Example Usage:
    yelp_cli.py 'mountain view, ca', 'bars' --keyfile=config/yelpkeys.json

    yelp_cli.py '(-37.3861, -122.0828)' 'bars' --loctype=GEO_COORD
            --keyfile=config/yelpkeys.json
'''

from yelpclient import YelpClient

import argparse
import ast
import json
import logging
import logging.config
import sys


class YelpCLI(object):
    '''Yelp Api Client client line interface
       Simple CLI to test the YelpClient api
    '''

    def __init__(self, yelp_api_keys):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = YelpClient(yelp_api_keys)

    def search(self, type, location, term):
        if type == 'LOCATION':
            result_json = self.client.search_by_location(
                location=location, term=term, limit=10,
                sort=YelpClient.SortType.BEST_MATCHED)
        elif type == 'GEO_COORD':
            latlong_tuple = ast.literal_eval(location)
            result_json = self.client.search_by_geo_coord(
                latlong=latlong_tuple, term='bars')
        else:
            raise ValueError('Invalid search type: %s' % type)

        if 'error' in result_json:
            self.logger.error(
                'API Client Error [%s]: %s'
                % (result_json['error']['id'], result_json['error']['text']))
        elif 'total' in result_json:
            self.logger.info('Total Results: ' + str(result_json['total']))

            for business in result_json['businesses']:
                self.logger.info(
                    'Id: %s, Name: %s, Rating: %s' %
                    (business['id'], business['name'], business['rating']))


if __name__ == '__main__':
    logging_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(module)s :' \
        + ' %(lineno)d - %(message)s'
    logging.basicConfig(level=logging.INFO, format=logging_fmt)

    parser = argparse.ArgumentParser(description='Yelp client line interface')
    parser.add_argument('--keyfile', dest='keyfile',
                        help='file containing the yelp api keys',
                        default=sys.prefix + '/cfg/yelp_keys.json')
    parser.add_argument('--loctype', dest='loctype',
                        choices=['LOCATION', 'GEO_COORD'],
                        help='search location type', default='LOCATION')
    parser.add_argument('location', help='search location value')
    parser.add_argument('term', help='search term')

    args = parser.parse_args()

    yelp_keys = json.load(open(args.keyfile))
    if yelp_keys['consumer_key'] == '__REPLACE__':
        print 'ERROR:Invalid api keys in %s' % args.keyfile
        sys.exit(-1)

    yelp_cli = YelpCLI(yelp_keys)
    yelp_cli.search(args.loctype, args.location, args.term)
