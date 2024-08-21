from django.urls import path

from roaster import views

urlpatterns = [
    path('', views.index, name='index'),
    path('roast', views.RoastOperations.as_view(), name='roast'),
]
