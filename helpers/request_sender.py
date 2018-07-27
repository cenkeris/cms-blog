import json
from pprint import pprint

import requests


def make_request(url, method, data, headers):
    if method == 'POST':
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
    elif method == 'GET':
        response = requests.get(url=url, headers=headers)
    elif method == 'PUT':
        response = requests.put(url=url, data=json.dumps(data), headers=headers)
    else:
        response = {}

    response_json = json.loads(response.text)

    if response.status_code != 200:
        pprint(response_json)

    return response_json


