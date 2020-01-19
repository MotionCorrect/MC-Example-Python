import json
import requests
import os
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# These are for the app setup in AD B2C
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

# This is the URI for this local app.
url_redirect = os.getenv("uri_redirect")

b2c_url_base = os.getenv("b2c_url_base")
url_authorization = f'{b2c_url_base}authorize'
url_token = f'{b2c_url_base}token'

api_url_base = os.getenv("api_url_base")


@app.route("/")
def demo():
    """
    Step 1: User Authorization.
    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    MoCoAPI = OAuth2Session(client_id)
    MoCoAPI.scope = f"{client_id} offline_access"
    MoCoAPI.redirect_uri="https://127.0.0.1:5000/callback"

    authorization_url, state = MoCoAPI.authorization_url(
        url_authorization,
        response_mode="query",
        nonce="anyRandomValue",
    )

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    # Thie authorization URL is the local callback path.
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """
    Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    MoCoAPI = OAuth2Session(
        client_id,
        state=session['oauth_state'])
    token = MoCoAPI.fetch_token(
        url_token,
        client_secret=client_secret,
        authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token
    print(f"Received Access token: {token}")

    import datetime


    with open("./access.json", "w") as f:
        f.write(json.dumps(token, indent=4))

    return redirect(url_for('.aknowledgement'))

@app.route("/aknowledgement", methods=["GET"])
def aknowledgement():
    """
    Tell the user that
    :return:
    """
    content="Thanks. Access token has been saved properly."
    return render_template("aknowledgement.html", content=content)

@app.route("/MCAPI", methods=["GET"])
def profile():
    """
    Step 4: Fetching a protected resource using an OAuth 2 token.
    """
    MoCoAPI = OAuth2Session(client_id, token=session['oauth_token'])



    return jsonify(MoCoAPI.get(f'{api_url_base}').json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(ssl_context='adhoc', debug=True)
