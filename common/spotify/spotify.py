import json
from base64 import b64encode
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from django.conf import settings

from api.models import SpotifyUser, Artist, Track
from common.spotify.dto import AccessTokenBody, TopArtistsResponse, TopTracksResponse, ArtistDetails, AlbumDetails, \
    ProfileResponse

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
def load_user_data(token: str):
    return executor.submit(_load_user_data, token)

# TODO Error handling everywhere
def _load_user_data(token: str):
    artists_data, tracks_data = _get_user_top_items(token)
    profile_data = get_user_profile(token)

    profile, _ = SpotifyUser.objects.get_or_create(id=profile_data.id, name=profile_data.display_name, profile_uri=profile_data.uri)


    for artist_data in artists_data:
        artist, _ = Artist.objects.get_or_create(id=artist_data.id, name=artist_data.name)
        if artist not in profile.artists.all():
            profile.artists.add(artist)


    for track_data_i in tracks_data:
        track_data = track_data_i.album
        track, _ = Track.objects.get_or_create(id=track_data.id, name=track_data.name)

        for track_artist in track_data.artists:
            artist, _ = Artist.objects.get_or_create(id=track_artist.id, name=track_artist.name)
            if artist not in track.artists.all():
                track.artists.add(artist)

        if track not in profile.tracks.all():
            profile.tracks.add(track)


def _get_user_top_items(token: str) -> tuple[list[ArtistDetails], list[AlbumDetails]]:
    url = "https://api.spotify.com/v1/me/top"
    limit = 5 # TODO: Figure perfect number

    # TODO: maybe cut artists out? Idk if super needed given the tracks have artists assigned to those
    artists_response = requests.get(f"{url}/artists?limit={limit}", headers={"Authorization": f"Bearer {token}"}).json()
    artists = (TopArtistsResponse
               .model_validate_json(json.dumps(artists_response))
               .items) # TODO Handle errors

    tracks_response = requests.get(f"{url}/tracks?limit={limit}", headers={"Authorization": f"Bearer {token}"}).json()
    tracks = (TopTracksResponse
              .model_validate_json(json.dumps(tracks_response))
              .items) # TODO Handle errors

    return artists, tracks

def get_user_profile(token: str) -> ProfileResponse:
    profile_response = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {token}"}).json()
    profile = ProfileResponse.model_validate_json(json.dumps(profile_response)) # TODO Handle errors
    return profile