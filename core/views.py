from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.conf import settings
def index(request: HttpRequest) -> HttpResponse:
    spotify_auth_url = ('https://accounts.spotify.com/authorize'
                        f'?client_id={settings.SPOTIFY_CLIENT_ID}'
                        '&response_type=code'
                        '&redirect_uri=http://localhost:8000/roast' # TODO: change later
                        '&scope=user-read-private%20user-read-email')
    return HttpResponse(render(request, "index.html", {"spotify_authorize_url": spotify_auth_url}))

def roast(request: HttpRequest) -> HttpResponse:
    code = request.GET.get('code')
    response = HttpResponse(render(request, "roast.html", {}))
    response.set_cookie("spotify_code", code)
    return response