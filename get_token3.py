# Pure requests. Nothing else.

import json
import requests
import os
from requests_oauthlib import OAuth2Session
from flask import Flask, redirect, session, url_for
from flask.json import jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# These are for the app setup in AD B2C
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

url_redirect = os.getenv("uri_redirect")

b2c_url_base = os.getenv("b2c_url_base")

url_authorization = f'{b2c_url_base}authorize'
url_token = f'{b2c_url_base}token'

api_url_base = os.getenv("api_url_base")
url=f'{url_authorization}?client_id={client_id}&nonce=anyRandomValue&redirect_uri=https://jwt.ms&scope={client_id}%20offline_access&response_type=code&response_mode=query'
outcome = requests.get(url)
print(url)