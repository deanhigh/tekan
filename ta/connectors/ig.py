import json
import logging
# from pprint import pprint

from datetime import timedelta
from pip._vendor.requests import Session

import requests
import requests_cache
# from trading_ig import IGService


# base_url = 'https://demo-api.ig.com/gateway/deal'
#
API_KEY = 'f6ea2f597dbad0acae302441c7c7abcd8406c9b8'
ACCOUNT_TYPE = 'DEMO'
IDENTIFIER = 'loathed_demo'


logging.basicConfig(level=logging.DEBUG)

expire_after = timedelta(hours=1)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
service = IGService(IDENTIFIER, 'Welcome1', API_KEY, ACCOUNT_TYPE)
service.create_session()

markets = service.fetch_historical_prices_by_epic_and_num_points('IX.D.FTSE.DAILY.IP', '1Min', 1000)
# print(markets['allowance'])
# print(markets['prices'])

# class IG(object):
#     _base_url =
#     def create_session(self, username, password, api_key):

# BASE_HEADER = {
#     'X-IG-API-KEY': API_KEY,
#     'Content-Type': 'application/json',
#     'Accept': 'application/json; charset=UTF-8'
# }
#604630
# session = Session()
# response = session.post(url=base_url,
#                         data=json.dumps(
#                             {
#                                 "identifier": "loathed_demo",
#                                 "password": "Welcome1"
#                             }),
#                         headers=BASE_HEADER)
#
# pprint(json.loads(response.text))
