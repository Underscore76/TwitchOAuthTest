import os
import json
from requests_oauthlib import OAuth2Session

from dotenv import load_dotenv

# needed because running locally, OAUTHLIB gets mad that we don't use https but
# running on localhost so http is fine
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# loads the .env file into os.environ dictionary
load_dotenv()

def get_refresh_client(scopes):
    oauth = OAuth2Session(
        client_id=os.environ['CLIENT_ID'],
        redirect_uri="http://localhost:3000",
        scope=scopes
    )
    # print(oauth.get('https://api.twitch.tv/helix/users'))
    authorization_url, state = oauth.authorization_url(
        "https://id.twitch.tv/oauth2/authorize",
    )
    print('click this url')
    print(authorization_url)
    auth_response = input("Copy paste the url from the address bar redirect here:\n")
    token = oauth.fetch_token(
        "https://id.twitch.tv/oauth2/token",
        authorization_response=auth_response,
        include_client_id=True,
        client_secret=os.environ['CLIENT_SECRET'],
    )

    # this session handles refreshing the underlying token for you
    client = OAuth2Session(
        client_id=os.environ['CLIENT_ID'],
        token=token, 
        auto_refresh_url="https://id.twitch.tv/oauth2/token",
        auto_refresh_kwargs={
            'client_id': os.environ['CLIENT_ID'],
            'client_secret': os.environ['CLIENT_SECRET'],
        },
    )
    return client, token

if __name__ == '__main__':
    scopes = [
        "chat:read",
        "chat:edit",
    ]
    client, token = get_refresh_client(scopes)
    print(json.dumps(token, indent=4))
    response = client.get(
        'https://api.twitch.tv/helix/users',
        headers={"Client-Id": os.environ['CLIENT_ID']}
    )
    print(client.token)
    print(response.json())
