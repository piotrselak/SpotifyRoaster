from django.urls import path

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('roast', views.roast, name='roast')
]
