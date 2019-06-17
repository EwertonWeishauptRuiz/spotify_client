import requests
import time
import json
from urllib.parse import urlparse
import os
from credentials import payload


def authorize_app(auth_code=None):
    scopes = [
        'user-modify-playback-state',
        'user-read-playback-state',
        'playlist-read-private',
        'playlist-read-collaborative',
        'streaming',
    ]

    print(
        "\nGo to the following url, and after clicking ok, copy and paste the"
        "link you are redirected to from your browser"
    )
    print(
        "\nhttps://accounts.spotify.com/authorize/?client_id=" +
        payload['client_id'] +
        "&response_type=code&redirect_uri=http://localhost&scope="
        + "%20".join(scopes)
    )
    url = input("\nPaste localhost url: ")
    parsed_url = urlparse(url)
    payload['grant_type'] = 'authorization_code'
    payload['code'] = parsed_url.query.split('=')[1]
    auth_code = {}

    response = requests.post(
        "https://accounts.spotify.com/api/token", data=payload)

    if response.status_code == 200:
        response_json = response.json()
        current_seconds = time.time()
        auth_code['expires_at'] = (
            current_seconds
            + response_json['expires_in']
            - 60)
        auth_code['access_token'] = response_json['access_token']

        if 'refresh_token' in response_json:
            auth_code['refresh_token'] = response_json['refresh_token']

        with open('auth.json', 'w') as output_file:
            json.dump(auth_code, output_file)
            return auth_code

        print('Sucessfuly Connects')
    else:
        raise Exception(
            'The status code was {}'.format({response.status_code}))


def get_valid_auth_header():
    with open('auth.json', 'r') as infile:
        auth = json.load(infile)
        if time.time() > auth['expires_at']:
            auth = authorize_app(auth)
        return {"Authorization": "Bearer " + auth["access_token"]}


if not os.path.isfile('auth.json'):
    auth = authorize_app()

authorize_app()
