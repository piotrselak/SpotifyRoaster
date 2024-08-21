import requests
from django.conf import settings
from django.core.cache import cache, BaseCache
from pydantic import BaseModel

# TODO: Handle exception when validation fails or something
def fetch_access_token() -> str:
    client_id = settings.SPOTIFY_CLIENT_ID
    secret = settings.SPOTIFY_CLIENT_SECRET
    response = requests.post("https://accounts.spotify.com/api/token",
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data={"grant_type": "client_credentials" , "client_id": client_id, "client_secret": secret}).json()

    validated_response = SpotifyAccessTokenResponse.model_validate_json(response)

    default_cache: BaseCache = cache
    default_cache.set("SPOTIFY_ACCESS_TOKEN", validated_response.access_token, validated_response.expires_in)

    return validated_response.access_token

class SpotifyAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int