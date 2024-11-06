from django.contrib import admin
from django.urls import path, include
from sentdex.views import DestinationView, RegisterView


urlpatterns = [
    path("", DestinationView.as_view(), name="index"),
    path('register/', RegisterView.as_view(), name='register'),
]
