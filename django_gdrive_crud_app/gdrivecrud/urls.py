from django.urls import path

from . import views

app_name = "gdrivecrud"
urlpatterns = [
    path("", views.index, name="index"),
    path("read/", views.read, name="read"),
]
