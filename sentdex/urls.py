from django.urls import path

from sentdex.views import (
    DestinationListView,
    DestinationView,
    LoginView,
    LogoutView,
    RegisterView,
    SearchView,
)

urlpatterns = [
    path("", DestinationView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "destination_list/<str:city_name>/",
        DestinationListView.as_view(),
        name="destination_list",
    ),
    path("search/", SearchView.as_view(), name="search"),


]
