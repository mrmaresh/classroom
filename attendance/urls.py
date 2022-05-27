from django.urls import path
from . import views



urlpatterns = [
path("", views.login, name="login"),
path("record", views.record, name="record"),
path("waitlist", views.waitlist, name="waitlist"),
path("dashboard", views.dashboard, name="dashboard"),
path("reset", views.reset, name="reset"),
path("schedule", views.schedule, name="schedule"),


# API Routes
path("select", views.select, name="select")
]