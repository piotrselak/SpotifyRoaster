import json
from base64 import b64encode
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from django.conf import settings

from common.spotify.dto import AccessTokenBody, TopArtistsResponse, TopTracksResponse, ArtistDetails, AlbumDetails

executor = ThreadPoolExecutor(max_workers=4) # TODO think about number here

def fetch_token(code: str) -> str:
    to_encode = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    encoded_bytes = b64encode(to_encode.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')

    response = requests.post("https://accounts.spotify.com/api/token",
                  headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {encoded_string}"},
                  data={"grant_type": "authorization_code", "code": code, "redirect_uri": settings.SPOTIFY_REDIRECT_URI})

    json_response = json.dumps(response.json())
    validated = AccessTokenBody.model_validate_json(json_response, strict=True) # TODO: Handle errors

    return validated.access_token # TODO Maybe remake into returning the rest as well


# TODO First check if data is already in database, if its older than 30 days, then refetch if not, use this data
# TODO: Probably move it so the items are fetched to db when user exits
def load_user_data(token: str):
    return executor.submit(_load_user_data, token)

def _load_user_data(token: str):
    artists, tracks = _get_user_top_items(token)

def _get_user_top_items(token: str) -> tuple[list[ArtistDetails], list[AlbumDetails]]:
    url = "https://api.spotify.com/v1/me/top"
    limit = 5 # TODO: Figure perfect number

    artists_response = requests.get(f"{url}/artists?limit={limit}", headers={"Authorization": f"Bearer {token}"}).json()
    artists = (TopArtistsResponse
               .model_validate_json(json.dumps(artists_response))
               .items) # TODO Handle errors

    tracks_response = requests.get(f"{url}/tracks?limit={limit}", headers={"Authorization": f"Bearer {token}"}).json()
    print(tracks_response)
    tracks = (TopTracksResponse
              .model_validate_json(json.dumps(tracks_response))
              .items) # TODO Handle errors

    return artists, tracks

def _get_user_profile():
    pass