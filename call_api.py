import json
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

# This is an example backend call to the MotionCorrect API services we have built.


# Load environmental variable.
load_dotenv()

# These are for the app setup in AD B2C
client_id = os.getenv("client_id")


api_url_base = os.getenv("api_url_base")

class MoCoAPISession():

    def __init__(self):
        self.session = None
        self.load_access_token()



    def load_access_token(self, path_default:Path = Path("./access.json")):
        """
        Load the access token from the default path
        :param path_default:
        :return:
        """
        with open(path_default) as json_data:
            token = json.load(json_data)
        self.session = OAuth2Session(client_id, token=token)

    def send_image(self, path_file:Path or str):
        """
        Send resources to the destination point using the path specified.
        :param path_file:
        :return:
        """
        path_file = Path(path_file)
        data = open(path_file, 'rb').read()
        response = self.session.post(api_url_base, data=data)
        print(response)

if __name__ == "__main__":
    session = MoCoAPISession()
    session.send_image(r"./test.png")