from django.urls import path
from . import views



urlpatterns = [
path("", views.login, name="login"),
path("record", views.record, name="record"),
path("waitlist", views.waitlist, name="waitlist"),
path("dashboard", views.dashboard, name="dashboard"),
path("schedule", views.schedule, name="schedule"),
path("restricted", views.restricted, name="restricted"),
path("choice", views.choice, name="choice"),
path("select", views.select, name="select"),
path("attendancePage", views.attendancePage, name="attendancePage"),
path("incidentPage", views.incidentPage, name="incidentPage"),
path("incident", views.incident, name="incident"),



# API Routes
path("attendance", views.attendance, name="attendance"),
path("checkNewPeriod", views.checkNewPeriod, name="checkNewPeriod"),
path("unexcused/<int:student_id>", views.unexcused, name="unexcused"),
path("resetWaitlist", views.resetWaitlist, name="resetWaitlist"),
path("resetAbsences", views.resetAbsences, name="resetAbsences"),
path("randomStudent", views.randomStudent, name="randomStudent"),
path("recordAbsence", views.recordAbsence, name="recordAbsence")
]