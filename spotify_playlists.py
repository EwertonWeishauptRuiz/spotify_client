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

def _clean_string(string):
    clean_string = string.replace(' ', '').lower()
    return clean_string

def get_tracks_in_playlist():
    headers = get_valid_auth_header()
    playlists = get_playlists()
    playlists_by_name = {}

    for playlist in playlists:
        name = _clean_string(playlist['name'])
        playlists_by_name[name] = playlist
        print(playlist['name'])

    playlist_name = input('Name of the playlist to get tracks from: \n\t->')
    playlist_name = _clean_string(playlist_name)

    if playlist_name in playlists_by_name:
        id_ = playlists_by_name[playlist_name]['id']
        tracks = requests.get(
            'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'.format(
                playlist_id=id_
            ), headers=headers
        ).json()
        for track in tracks['items']:
            name = track['track']['name']
            band = track['track']['artists'][0]['name']
            # Make a for loop on all artists, as it can be more than one before
            # GEtting the name
            # Append to a list all the tracks.

            
            import pdb; pdb.set_trace()
        import pdb; pdb.set_trace()
        print('yes')
    else:
        print('no')

        
get_tracks_in_playlist()
