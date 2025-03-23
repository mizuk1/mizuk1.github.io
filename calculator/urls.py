from django.urls import path
from . import views

urlpatterns = [
    path("", views.dps_view, name="index"),
]