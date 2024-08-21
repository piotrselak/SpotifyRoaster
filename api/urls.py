from django.urls import path

from api import views

urlpatterns = [
    path('', views.RoastOperations.as_view(), name='RoastOperations'),
]
