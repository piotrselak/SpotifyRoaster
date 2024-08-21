from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


def index(request: WSGIRequest) -> HttpResponse:
    """The whole purpose of this view is to return htmx template which
    handles all the logic"""
    return HttpResponse(render(request, "index.html"))

# It should be called automatically every hour
#def _fetch_spotify_api_token()

class RoastOperations(APIView):
    def get(self, request) -> Response:
        return Response("Hello World2")