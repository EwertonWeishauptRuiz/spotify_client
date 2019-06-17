import requests

from api_connect import get_valid_auth_header

def get_playlists(offset=None):
    params = {}
    params['limit'] = 50
    user_playlists = []
    headers = get_valid_auth_header()

    playlists = requests.get(
        "https://api.spotify.com/v1/me/playlists",
        headers=headers,
        params=params).json()

    for playlist in playlists['items']:
        user_playlists.append(playlist)

    next_page = playlists['next']
    while next_page:
        request = requests.get(next_page, headers=headers).json()
        for item in request['items']:
            user_playlists.append(item)
        next_page = request['next']

    return user_playlists

def get_amount_playlists():
    playlists = get_playlists()
    return len(playlists)

print(get_amount_playlists())
