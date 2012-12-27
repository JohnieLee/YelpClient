from __init__ import YelpClient

import logging
import logging.config
import yelp_config


if __name__ == '__main__' :
    logging_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s'
    logging.basicConfig(level = logging.DEBUG, format=logging_fmt)
    logger = logging.getLogger(__name__)

    client = YelpClient(yelp_config.keys)
    #result_json = client.search_by_location(
    #    location = '94043', term = 'Red Room', limit = 10, 
    #    sort = YelpClient.SortType.BEST_MATCHED)

    result_json = client.search_by_geo_coord(latlong = (39.0639, -108.55), term='bars')

    if 'total' in result_json :
        logger.info("Total Results: " + str(result_json['total']))

        for business in result_json['businesses'] :
            logger.info('Id: %s, Name: %s, Rating: %s' 
                % (business['id'], business['name'], business['rating']))
        
        
