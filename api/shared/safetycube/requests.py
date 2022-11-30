import requests
import urllib
from constance import config
from urllib.parse import quote

from .constants import *


def api_call_hook(response, *args, **kwargs):
    try:
        r = response.json()
        raise ValueError("{} : {}".format(r['errorType'], r['message']))
    except:
        response.raise_for_status()


def make_session():
    url = SAFETYCUBE_LOGIN_PATTERN.format(root_url=config.SAFETYCUBE_URL)
    session = requests.session()
    session.proxies = urllib.request.getproxies()
    session.hooks = {
        'response': api_call_hook
    }
    session.get(url, auth=(config.SAFETYCUBE_USERNAME,
                           config.SAFETYCUBE_PASSWORD))
    return session


def create(session, payload):
    url = SAFETYCUBE_CREATE_FORM_PATTERN.format(root_url=config.SAFETYCUBE_URL)
    r = session.put(url, json=payload, headers={
                    'Content-type': 'application/json'})
    return r.json()


def update(session, reference, payload):
    url = SAFETYCUBE_UPDATE_FORM_PATTERN.format(
        root_url=config.SAFETYCUBE_URL) + quote(reference, safe="")
    r = session.post(url, json=payload, headers={
                     'Content-type': 'application/json'})
    return r.json()


def get_status(session, reference):
    url = SAFETYCUBE_FORM_STATUS_PATTERN.format(
        root_url=config.SAFETYCUBE_URL) + quote(reference, safe="")
    r = session.get(url)
    return r.json()
