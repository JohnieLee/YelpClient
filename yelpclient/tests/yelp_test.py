from yelpclient import YelpClient

import logging
import logging.config
import mock
import oauth2
import unittest


class YelpClientTest(unittest.TestCase):

    def setUp(self):
        self.keys = {
            'consumer_key': 'value1',
            'consumer_secret': 'value2',
            'token': 'value3',
            'token_secret': 'value4'}
        self.client = YelpClient(self.keys)

    @mock.patch("yelpclient.client.oauth2.generate_nonce")
    @mock.patch("yelpclient.client.time.time")
    @mock.patch("yelpclient.client.requests")
    def test_search_by_location(self, mock_requests, mock_time, mock_oauth2):
        # Setup
        expected_url = self._sign_request(
            YelpClient._search_api_path + 'location=FOO&term=bars')

        mock_oauth2.return_value = 2000
        mock_time.return_value = 1000

        # Run
        result = self.client.search_by_location(location='FOO', term='bars')

        # Verify
        mock_time.assert_called_with()
        mock_requests.get.assert_called_with(expected_url)

        self.assertTrue(mock_requests.get.return_value.json.called)
        self.assertEqual(mock_requests.get.return_value.json.return_value,
                         result)

    def test_search_by_location_missing_location(self):
        '''Tests that search_by_location raises ValueError
           for no location arg
        '''
        self.assertRaises(ValueError, self.client.search_by_location, None)

    @mock.patch("yelpclient.client.oauth2.generate_nonce")
    @mock.patch("yelpclient.client.time.time")
    @mock.patch("yelpclient.client.requests")
    def test_search_by_geo_coord(self, mock_requests, mock_time, mock_oauth2):
        # Setup
        expected_url = self._sign_request(
            YelpClient._search_api_path + 'll=39.0639,-108.55&term=bars')

        mock_oauth2.return_value = 2000
        mock_time.return_value = 1000

        # Run
        result = self.client.search_by_geo_coord(latlong=(39.0639, -108.55),
                                                 term='bars')

        # Verify
        mock_time.assert_called_with()
        mock_requests.get.assert_called_with(expected_url)

        self.assertTrue(mock_requests.get.return_value.json.called)
        self.assertEqual(mock_requests.get.return_value.json.return_value,
                         result)

    def test_search_by_geo_coord_missing_latlong(self):
        '''Tests that search_by_location raises ValueError
           for no geo coord arg
           '''
        self.assertRaises(ValueError, self.client.search_by_geo_coord, None)
        self.assertRaises(ValueError, self.client.search_by_geo_coord,
                          (123.55,))

    def _sign_request(self, url):
        consumer_key = oauth2.Consumer(self.keys['consumer_key'],
                                       self.keys['consumer_secret'])
        token = oauth2.Token(self.keys['token'],
                             self.keys['token_secret'])
        oauth_params = {
            'oauth_nonce': 2000,
            'oauth_timestamp': 1000,
            'oauth_token': token.key,
            'oauth_consumer_key': consumer_key.key,
        }

        request = oauth2.Request('GET', url, oauth_params)
        request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(),
                             consumer_key, token)
        return request.to_url()


def main():
    unittest.main()

if __name__ == '__main__':
    logging_fmt = '%(asctime)s - %(name)s - %(levelname)s - " \
            + "%(module)s: %(lineno)d - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_fmt)
    logger = logging.getLogger(__name__)

    main()
