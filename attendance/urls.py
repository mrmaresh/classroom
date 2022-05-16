from django.urls import path
from . import views



urlpatterns = [
path("", views.login, name="login"),
path("record", views.record, name="record"),


# API Routes
path("select", views.select, name="select")
]