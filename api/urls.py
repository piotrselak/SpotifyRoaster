from django.urls import path

from api import views

urlpatterns = [
    path('generate', views.RoastGenerator.as_view(), name='generator'),
]
