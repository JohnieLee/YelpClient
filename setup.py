from setuptools import setup

setup(
    name = 'yelp api client',
    version = '0.0.1',
    author = 'Johnie Lee',
    author_email = 'johnie@johnia.com',
    description = 'Client library for Yelp API',
    url = 'https://github.com/tazzy531/YelpClient',
    packages = ['yelpclient', ],
    test_suite = 'yelpclient.tests',
)

