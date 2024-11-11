from django.contrib import admin
from django.urls import path, include
from sentdex.views import (
    DestinationView,
    RegisterView,
    LoginView,
    LogoutView,
    DestinationListView,
)

urlpatterns = [
    path("", DestinationView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "destination_list/<str:city_name",
        DestinationListView.as_view(),
        name="destination_list",
    ),
]
if __name__ == "__main__":
    main()
