from django.http import HttpRequest
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SpotifyUser, Track
from common.openai import generate_roast
from common.spotify import get_user_profile


# TODO add check if the user is logged via spotify

class RoastGenerator(APIView):
    @staticmethod
    def post(request: HttpRequest) -> Response:
        spotify_token = request.headers.get('Authorization')
        if not spotify_token:
            return Response("Token missing", status=status.HTTP_401_UNAUTHORIZED)

        spotify_token = spotify_token.split('Bearer ')[1]

        user_profile = get_user_profile(spotify_token) # TODO ERROR HANDLING
        user = get_object_or_404(SpotifyUser, pk=user_profile.id)

        # TODO what if user logged second time after a few months so the artists would differ
        artists = user.artists.all()
        tracks = user.tracks.all()

        parsed_artists = map(lambda artist: artist.name, artists)

        parsed_tracks = list(map(
            lambda track: f"{track.name} by {', '.join(artist.name for artist in track.artists.all())}",
            tracks
        ))

        prompt = ("Roast this spotify user based on this data. "
                  f"Top user artists: {",".join(parsed_artists)}. "
                  f"Top tracks: {",".join(parsed_tracks)}")

        roast = generate_roast("You are a sassy, sarcastic roast comedian.", prompt)

        return Response({"roast": roast.content})