from django.urls import path

from roaster import views

urlpatterns = [
    path('', views.index, name='index')
]
