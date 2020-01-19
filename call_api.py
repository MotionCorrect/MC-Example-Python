import json
import os
from pathlib import Path
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

# This is an example backend call to the MotionCorrect API services we have built.


# Load environmental variable.
load_dotenv()

# Load base URL for the policy
b2c_url_base = os.getenv("b2c_url_base")

# Set the URL for getting/refereshing the token.
url_token = f'{b2c_url_base}token'

# These are for the app setup in Azure AD B2C
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

api_url_base = os.getenv("api_url_base")

class MoCoAPISession():

    def __init__(self):
        # Initialize the session by loading the existing access token.
        self.session: OAuth2Session = None
        self.load_access_token()

    def load_access_token(self, path_default:Path = Path("./access.json")):
        """
        Load the access token from the default path with default name.
        :param path_default:
        :return:
        """

        # Load the json file as token.
        with open(path_default) as json_data:
            token = json.load(json_data)

        # Set session using the client ID and the token.
        self.session = OAuth2Session(client_id, token=token)

    def send_image(self, path_file: Path or str):
        """
        Send resources to the destination point using the path specified.
        :param path_file:
        :return:
        """
        # Force path to be Path.
        path_file = Path(path_file)

        # Open the data for reading as blob
        data = open(path_file, 'rb').read()

        try:
            # Try to post with existing session information with previously saved access token.
            response = self.session.post(api_url_base, data=data)
            # If all goes well, return the response.
            print("Existing access token seems valid.")

        except TokenExpiredError as e:

            # Access token can expire QUITE easily (60 mins)
            print("Existing access token no longer valid.")
            print("Refreshing token using freshing token.")

            # Requesting refresh token.
            refreshed_token = self.session.refresh_token(
                token_url=url_token,
                client_secret=client_secret,
            )

            print("Successfully obtained new access token.")
            print("Writting refreshed token.")
            # Write out the updated token.
            with open("./access.json", "w") as f:
                f.write(json.dumps(refreshed_token, indent=4))

            # Print out the response now that everything is back on track.
            response = self.session.post(api_url_base, data=data)

            print("New access token seems working.")

        print(response.text)

if __name__ == "__main__":
    session = MoCoAPISession()
    session.send_image(r"./test.png")