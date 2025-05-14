from django.urls import path

from .views import (
    DoctorProfileView,
    DoctorsListView
)

app_name = "doctors"

urlpatterns = [
    path("", DoctorsListView.as_view(), name="list"),
    path(
        "<str:username>/profile/",
        DoctorProfileView.as_view(),
        name="doctor-profile",
    )
]
