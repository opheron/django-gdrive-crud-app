from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "gdrivecrud"
urlpatterns = [
    path("", views.index, name="index"),
    path("delete/", views.delete, name="delete"),
    # path(
    #     "list/",
    #     TemplateView.as_view(template_name="gdrivecrud/list.html"),
    #     name="list",
    # ),
    # path("list/", views.list, name="list"),
    # path("read/", views.read, name="read"),
]
