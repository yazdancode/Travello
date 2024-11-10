from django.contrib import admin
from django.urls import path, include
from sentdex.views import DestinationView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path("", DestinationView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
