import json
import requests
import os
from requests_oauthlib import OAuth2Session

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
url_redirect = os.getenv("url_redirect")

url_authorization = 'https://motioncorrectb2c.b2clogin.com/motioncorrectb2c.onmicrosoft.com/b2c_1_api_authentication/oauth2/v2.0/authorize'
url_token = 'https://motioncorrectb2c.b2clogin.com/motioncorrectb2c.onmicrosoft.com/b2c_1_api_authentication/oauth2/v2.0/token'

api_token = os.getenv("token")
api_url_base = os.getenv("url_api")

MoCoAPI = OAuth2Session(client_id)
url_authorization, state = MoCoAPI.authorization_url(url_authorization)
print('Please go here and authorize,', url_authorization)

redirect_response = input('Paste the full redirect URL here:')
MoCoAPI.fetch_token(
    url_token,
    client_secret=client_secret,
    authorization_response=redirect_response
)


# Fetch a protected resource, i.e. user profile
r = github.get('https://api.github.com/user')

scope = "openid"


headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}

def get_account_info():

    api_url = '{0}account'.format(api_url_base)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

if __name__=="__main__":
    if account_info is not None:
        print("Here's your info: ")
        for k, v in account_info['account'].items():
            print('{0}:{1}'.format(k, v))




from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage

CLIENT_ID = '<Client ID from Google API Console>'
CLIENT_SECRET = '<Client secret from Google API Console>'


flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           scope='https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
                           redirect_uri='http://example.com/auth_return')

storage = Storage('creds.data')

credentials = run(flow, storage)

print "access_token: %s" % credentials.access_token