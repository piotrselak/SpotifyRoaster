from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

def index(request: WSGIRequest) -> HttpResponse:
    """The whole purpose of this view is to return htmx template which
    handles all the logic"""
    return HttpResponse(render(request, "index.html"))

