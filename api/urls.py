from django.urls import path

from api import views

urlpatterns = [
    path('generate', views.APIView.as_view(), name='generator'),
]
