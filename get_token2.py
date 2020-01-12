from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv

load_dotenv()

# These are for the app setup in AD B2C
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

#url_redirect = os.getenv("url_redirect")

# Get base URL and URI redirect
b2c_url_base = os.getenv("b2c_url_base")
uri_redirect = os.getenv("uri_redirect")

# Update the base URL to form the authorization and token endpoints.
authorization_base_url = f'{b2c_url_base}authorize'
url_token = f'{b2c_url_base}token'

api_url_base = os.getenv("api_url_base")

#  Form the query with the proper parameters:
MC_API = OAuth2Session(client_id)
MC_API.redirect_uri = uri_redirect
MC_API.scope = f"{client_id} offline_access"
# Redirect user to GitHub for authorization
authorization_url, state = MC_API.authorization_url(authorization_base_url,
                                                    response_mode="query")
print('Please go here and authorize,', authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input('Paste the full redirect URL here:')

# Fetch the access token
MC_API.fetch_token(url_token,
                   client_secret=client_secret,
                   authorization_response=redirect_response,
                   state=state)

# Fetch a protected resource, i.e. user profile
r = MC_API.get(f"{authorization_base_url}?client_id={client_id}&nonce=")