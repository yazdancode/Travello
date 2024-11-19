from django.urls import path

from sentdex.views import (
    DestinationListView,
    DestinationView,
    LoginView,
    LogoutView,
    RegisterView,
    SearchView,
    DestinationDetailsView,
    PassengerDetailView,
    UpcomingTripsView,
    CardPaymentView,
    OTPVerificationView,
    NetBankingPaymentView,
    AboutView,
    BlogView,
    SingleBlogView,
    ContactView,
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
    path(
        "destination_list/destination_details/<str:city_name>",
        DestinationDetailsView.as_view(),
        name="destination_details",
    ),
    path(
        "destination_details/<str:city_name>",
        DestinationDetailsView.as_view(),
        name="destination_details",
    ),
    path(
        "destination_list/destination_details/pessanger_detail_def/<str:city_name>",
        PassengerDetailView.as_view(),
        name="pessanger_detail_def",
    ),
    path("upcoming_trips", UpcomingTripsView.as_view(), name="upcoming_trips"),
    path(
        "destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/card_payment",
        CardPaymentView.as_view(),
        name="card_payment",
    ),
    path(
        "destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/otp_verification",
        OTPVerificationView.as_view(),
        name="otp_verification",
    ),
    path(
        "destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/net_payment",
        NetBankingPaymentView.as_view(),
        name="net_payment",
    ),
    path("about/", AboutView.as_view(), name="about"),
    path("blog/", BlogView.as_view(), name="blog"),
    path("single-blog/", SingleBlogView.as_view(), name="single-blog"),
    path("contact/", ContactView.as_view(), name="contact"),
]
