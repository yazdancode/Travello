from django.contrib import admin
from django.urls import path, include
from sentdex.views import DestinationView


urlpatterns = [
    path('', DestinationView.as_view(), name='index'),
]
