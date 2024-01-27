import os
import json
from requests_oauthlib import OAuth2Session
import requests
from urllib.parse import urlencode, urlparse, parse_qs
from dotenv import load_dotenv

# loads the .env file into os.environ dictionary
load_dotenv()

def get_implicit_token(scopes):
    state = OAuth2Session().new_state()

    authorization_url = "https://id.twitch.tv/oauth2/authorize?" + urlencode({
        "client_id": os.environ['CLIENT_ID'],
        "redirect_uri": "http://localhost:3000",
        "response_type": "token",
        "scope": " ".join(scopes),
        "state": state,
    })

    print('click this url:')
    print(authorization_url)
    auth_response = input('To validate your token: paste the url from the address bar redirect here (otherwise enter to exit):\n')
    if auth_response == "":
        exit(0)
    
    fragment = urlparse(auth_response).fragment
    query = parse_qs(fragment)
    access_token = query['access_token'][0]

    # check that the state matches (meant to address CSRF attacks)
    assert query["state"][0] == state

    response = requests.get(
        'https://id.twitch.tv/oauth2/validate',
        headers={"Authorization": f"OAuth {access_token}"}
    )
    print(json.dumps(response.json(), indent=4))
    return access_token

if __name__ == '__main__':
    scopes = [
        "chat:read",
        "chat:edit",
    ]
    # this token lasts for 60 days!
    access_token = get_implicit_token(scopes)
    print(access_token)