from yelp import YelpClient

import logging
import logging.config
import yelp_config


logging_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s'
logging.basicConfig(level = logging.DEBUG, format=logging_fmt)
logger = logging.getLogger(__name__)

if __name__ == '__main__' :
    client = YelpClient(yelp_config.keys)
    result_json = client.search_by_location(
        location = '94043', term = 'Red Room', limit = 10, 
        sort = YelpClient.SortType.BEST_MATCHED)

    logger.info("Total Results: " + str(result_json['total']))

    for business in result_json['businesses'] :
        logger.info('Id: %s, Name: %s, Rating: %s' 
            % (business['id'], business['name'], business['rating']))
        
        