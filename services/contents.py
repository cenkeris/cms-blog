import json

import requests
from flask import session
from markupsafe import Markup

from helpers.request_sender import make_request


def get_contents_from_api(page):
    limit = 20
    skip = (page - 1) * limit
    delivery_api = 'http://dev-delivery.dogannet.tv/api/domains/'
    domain_id = '5b4c7527e138238fd0b64328'
    content_api = '/contents/_query'
    query_string = '?limit={}&skip={}&sort=sys.published_at desc'.format(limit, skip)
    url = delivery_api + domain_id + content_api + query_string

    where = {
        'where': {
            'type': 'haberler'
        }
    }

    headers = {
        'Authorization': 'Basic 5b4c762fe138238fd0b643e9:4ADWN0IY7GOXSNQCazqa'
    }
    response = requests.post(url=url, data=json.dumps(where), headers=headers)

    response_json = json.loads(response.text)

    return response_json['data']['items']


def get_contents_from_url(r_url):
    delivery_api = 'http://dev-delivery.dogannet.tv/api/domains/'
    domain_id = '5b4c7527e138238fd0b64328'
    router_string = '/router?url=/{}'.format(r_url)
    r_url = delivery_api + domain_id + router_string
    headers = {
        'Authorization': 'Basic 5b4c762fe138238fd0b643e9:4ADWN0IY7GOXSNQCazqa'
    }

    response = make_request(r_url, 'GET', data=None, headers=headers)
    response['model']['metin'] = Markup(response['model']['metin'])
    return response['model']


def get_contents_from_about(u_url):
    delivery_api = 'http://dev-delivery.dogannet.tv/api/domains/'
    domain_id = '5b4c7527e138238fd0b64328'
    router_string = '/router?url=/{}'.format(u_url)
    u_url = delivery_api + domain_id + router_string

    headers = {
        'Authorization': 'Basic 5b4c762fe138238fd0b643e9:4ADWN0IY7GOXSNQCazqa'
    }
    response = requests.get(u_url, headers=headers)
    response_json = json.loads(response.text)
    return response_json['model']


def get_contents_from_contact(t_url):
    delivery_api = 'http://dev-delivery.dogannet.tv/api/domains/'
    domain_id = '5b4c7527e138238fd0b64328'
    router_string = '/router?url=/{}'.format(t_url)
    t_url = delivery_api + domain_id + router_string

    headers = {
        'Authorization': 'Basic 5b4c762fe138238fd0b643e9:4ADWN0IY7GOXSNQCazqa'
    }
    response = requests.get(t_url, headers=headers)
    response_json = json.loads(response.text)
    return response_json['model']


def get_contents_from_login(g_url):
    delivery_api = 'http://dev-delivery.dogannet.tv/api/domains/'
    domain_id = '5b4c7527e138238fd0b64328'
    router_string = '/router?url=/{}'.format(g_url)
    g_url = delivery_api + domain_id + router_string

    headers = {
        'Authorization': 'Basic 5b4c762fe138238fd0b643e9:4ADWN0IY7GOXSNQCazqa'
    }
    response = requests.get(g_url, headers=headers)
    response_json = json.loads(response.text)
    return response_json


def get_token(credentials):
    management_api = 'http://dev-management.dogannet.tv/api/tokens'
    headers = {
        "Content-Type": 'application/json'
    }
    response = make_request(management_api, 'POST', data=credentials, headers=headers)

    token = response.get('token')
    return token


def get_user(token):
    management_api = 'http://dev-management.dogannet.tv/api/me'

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.get(management_api, headers=headers)

    if response.status_code != 201:
        return False

    response_json = json.loads(response.text)
    return response_json['user']


def update_content(content, comment):

    if not session.get('token'):
        if not session.get('user'):

            return
    url = "http://dev-management.dogannet.tv/api/domains/{}/contents/{}".format(content['domain_id'], content['_id'])

    yorumlar_alani = content.get('comment', [])
    yorum = {
        'uzunmetin': comment
    }

    yorumlar_alani.append(yorum)

    data = {
        'comment': yorumlar_alani
    }

    headers = {
        'Authorization': 'Bearer {}'.format(session['token']),
        'X-Update-Version': str(content['sys']['version'])
    }

    response = requests.put(url, data=json.dumps(data), headers=headers)
    response_json = json.loads(response.text)
    publish_url = "http://dev-management.dogannet.tv/api/domains/{}/published-contents".format(content['domain_id'])
    body = {
        '_id': response_json['_id']
    }

    response = requests.post(publish_url, data=json.dumps(body), headers=headers)

    response_json = json.loads(response.text)
    response_json['metin'] = Markup(response_json['metin'])
    return response_json
