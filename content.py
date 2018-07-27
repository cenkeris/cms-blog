import json
from pprint import pprint
import requests
from flask import Markup


def make_request(url, method, data=None):
    headers = {
        'Authorization': 'Basic 5b460be9e13823a84ff3385f:PxrmGqpgqsmqtGjm57oP'
    }

    if method == 'POST':
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
    elif method == 'GET':
        response = requests.get(url=url, headers=headers)
    else:
        response = {}

    response_json = json.loads(response.text)

    if response.status_code != 200:
        pprint(response_json)

    return response_json


def get_last_item():
    url = 'http://dev-delivery.dogannet.tv/api/domains/5b4605cde13823a84ff3359d/contents/_query?limit=1&sort=sys.published_at desc'
    where = {
        'where': {
            'type': 'haberler'
        }
    }
    response_json = make_request(url, 'POST', data=where)
    if response_json['data']['count'] != 0:
        return response_json['data']['items'][0]
    else:
        return []


def get_contents():
    url = 'http://dev-delivery.dogannet.tv/api/domains/5b4605cde13823a84ff3359d/contents/_query?sort=sys.published_at desc'

    where = {
        'where': {
            'type': 'haberler'
        }
    }

    response = make_request(url, 'POST', data=where)

    return response['data']['items']


def get_content_by_url(url):
    r_url = 'http://dev-delivery.dogannet.tv/api/domains/5b4605cde13823a84ff3359d/router?url=/{}'.format(url)
    response = make_request(r_url, 'GET', data=None)

    response['model']['guncel'] = Markup(response['model']['guncel'])

    return response['model']
