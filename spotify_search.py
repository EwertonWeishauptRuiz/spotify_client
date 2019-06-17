import requests

from urllib import parse
from api_connect import get_valid_auth_header


def spotify_search(name, search_type):
    headers = get_valid_auth_header()
    url = 'https://api.spotify.com/v1/search?q={}&type={}'.format(
            parse.quote(name),
            parse.quote(search_type),
        )
    request = requests.get(url, headers=headers).json()
    [item['name'] for item in request['artists']['items']]
    import pdb; pdb.set_trace()
