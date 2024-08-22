from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.conf import settings

from common.spotify import load_user_data, fetch_token


def index(request: HttpRequest) -> HttpResponse:
    spotify_auth_url = ('https://accounts.spotify.com/authorize'
                        f'?client_id={settings.SPOTIFY_CLIENT_ID}'
                        '&response_type=code'
                        f'&redirect_uri={settings.SPOTIFY_REDIRECT_URI}' # TODO: change later
                        '&scope=user-top-read')
    return HttpResponse(render(request, "index.html", {"spotify_authorize_url": spotify_auth_url}))

def roast(request: HttpRequest) -> HttpResponse:
    code = request.GET.get(key="code")
    token = fetch_token(code)
    load_user_data(token) # TODO: Secure stuff if token is not here etc.

    response = HttpResponse(render(request, "roast.html", {}))
    response.set_cookie("token", token)

    return response