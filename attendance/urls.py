from django.urls import path
from . import views



urlpatterns = [
path("", views.login, name="login"),
path("record", views.record, name="record"),
path("waitlist", views.waitlist, name="waitlist"),
path("dashboard", views.dashboard, name="dashboard"),
path("reset", views.reset, name="reset"),
path("schedule", views.schedule, name="schedule"),
path("restricted", views.restricted, name="restricted"),
path("choice", views.choice, name="choice"),
path("select", views.select, name="select"),
path("attendancePage", views.attendancePage, name="attendancePage"),


# API Routes
path("attendance", views.attendance, name="attendance"),
path("unexcused", views.unexcused, name="unexcused")
]