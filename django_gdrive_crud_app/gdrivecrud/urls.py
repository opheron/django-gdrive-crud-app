from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "gdrivecrud"
urlpatterns = [
    path("", views.index, name="index"),
    path("delete/", views.delete, name="delete"),
    path("upload/", views.upload, name="upload"),
]
