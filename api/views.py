from django.http import HttpRequest
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SpotifyUser
from common.spotify import get_user_profile


# TODO add check if the user is logged via spotify

class RoastGenerator(APIView):
    @staticmethod
    def post(request: HttpRequest) -> Response:
        spotify_token = request.headers.get('Authorization')
        if not spotify_token:
            return Response("Token missing", status=status.HTTP_401_UNAUTHORIZED)

        user_profile = get_user_profile(spotify_token) # TODO ERROR HANDLING
        user = get_object_or_404(SpotifyUser, pk=user_profile.id)

        # TODO what if user logged second time after a few months so the artists would differ
        artists = user.artists.all()
        tracks = user.artists.all()