from django.urls import path
from .views import pred

app_name = "model"

urlpatterns = [
    path("", pred, name="model"),
]
