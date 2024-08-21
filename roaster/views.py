from django.http import HttpResponse
from django.shortcuts import render

def index(request): # TODO: this one will return htmx template
    return HttpResponse(render(request, "index.html"))

