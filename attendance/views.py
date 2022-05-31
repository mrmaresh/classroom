import json
import time
from datetime import datetime, timedelta, timezone, time, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count





# Create your views here.

from .models import Student, Record, Bathroom, Waitlist, Schedule

# ISSUE:  what period is detected during passing period?
# Create a function that sets the default schedule and have it automatically run every morning prior to school
# Create a function that resets the waitlist every change of period automatically



def get_current_period():

    now = datetime.now()

    period = ['period_0', 'period_1', 'period_2', 'period_3', 'period_4', 'period_5', 'period_6', 'period_7', 'period_8']
    for i in range(9):
        then = datetime.strptime(getattr(Schedule.objects.get(active = True), period[i]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)  - timedelta(minutes=7)
        if now < then:
            return [period[i-1], period[i]]

    return ['period_0', 'period_1']



def restricted(request):
    return render(request, "restricted.html")



@login_required(login_url='restricted')
def login(request):
    period = get_current_period()
    start = datetime.strptime(getattr(Schedule.objects.get(active = True), period[0]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year) - timedelta(minutes=7)
    finish = datetime.strptime(getattr(Schedule.objects.get(active = True), period[1]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
    students = []

    record_query = Record.objects.values('student_id').annotate(dcount=Count('student_id'))


    if len(record_query) > 0:
        for record in record_query:
            student = Student.objects.get(pk = record['student_id'])
            records = Record.objects.filter(student=student, timestamp__range = [start,finish]).order_by('-timestamp')
            if len(records) > 0:
                if records[0].reason == "use_restroom":
                    name = Student.objects.get(pk = record['student_id']).first
                    students.append(name)

    if len(students) > 0:
        in_use = True
    else:
        in_use = False

    if len(Waitlist.objects.all()) > 0:
        waiting = True
    else:
        waiting = False

    val = Record.objects.all().first().timestamp.time
    datetime.strptime("11:31AM", '%I:%M%p')
    now = datetime.now()
    '''
    then = datetime.strptime(Schedule.objects.get(schedule = "regular").period_1, '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
    '''
    return render(request, "login.html",{
        "students": students,
        "in_use": in_use,
        "waitlist": Waitlist.objects.all(),
        "waiting": waiting,
        "records": Record.objects.filter(timestamp__range = [start,finish]),
        "period": get_current_period(),
        "start": start,
        "finish": finish,
        "student_query": datetime.strptime(getattr(Schedule.objects.get(active=True), 'period_1'), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
    })




def is_returning(records):
    if len(records) > 0:
        if records[0].reason == "use_restroom":
            return True
        else:
            return False
    else:
        return False



@login_required
def select(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        in_use = request.POST["in_use"]
        if len(Student.objects.filter(student_id=student_id)) == 0:
            messages.add_message(request, messages.INFO, 'Incorrect Student ID.')
            return HttpResponseRedirect(reverse("login"))
        else:
            student = Student.objects.get(student_id=student_id)
            period = get_current_period()
            start = datetime.strptime(getattr(Schedule.objects.get(active = True), period[0]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year) - timedelta(minutes=7)
            finish = datetime.strptime(getattr(Schedule.objects.get(active = True), period[1]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
            records = Record.objects.filter(student=student, timestamp__range = [start,finish]).order_by('-timestamp')
            returning = is_returning(records)
            return render(request, 'select.html',{
                "student": student,
                "returning": returning,
                "usage": Bathroom.objects.filter(student=student).order_by('-time_out'),
                "in_use": in_use
            })


def waitlist(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        student = Student.objects.get(student_id = student_id)
        if len(Waitlist.objects.filter(student=student)) == 0:
            entry = Waitlist.objects.create(student = student)
            entry.save()
        return HttpResponseRedirect(reverse("login"))


def reset(request):
    if request.method == "POST":
        Waitlist.objects.all().delete()
        return HttpResponseRedirect(reverse("dashboard"))


@login_required
def dashboard(request):
    period = get_current_period()
    start = datetime.strptime(getattr(Schedule.objects.get(active = True), period[0]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)  - timedelta(minutes=7)
    finish = datetime.strptime(getattr(Schedule.objects.get(active = True), period[1]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
    startdate = datetime.today()-timedelta(hours=8)
    records = Bathroom.objects.filter(time_out__gt = startdate).order_by('-time_out')
    return render(request, 'dashboard.html',{
        "waitlist": Waitlist.objects.all(),
        "records": records,
        "startdate":startdate.date,
        "hour": datetime.now().hour,
        "minute": datetime.now().minute,
        "schedule": Schedule.objects.get(active=True).schedule,
        "recordz": Record.objects.filter(timestamp__range = [start,finish]),
        "period": get_current_period(),
        "start": start,
        "finish": finish,
    })


def schedule(request):
    if request.method == "POST":
        active = Schedule.objects.get(active = True)
        active.active = False
        active.save()
        schedule = request.POST["schedule"]
        change = Schedule.objects.get(schedule = schedule)
        change.active = True
        change.save()
        return HttpResponseRedirect(reverse("dashboard"))




def record(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        reason = request.POST["reason"]
        student = Student.objects.get(student_id=student_id)
        record = Record.objects.create(student=student, reason=reason)
        record.save()
        if reason == "use_restroom":
            if len(Waitlist.objects.filter(student=student)) == 1:
                Waitlist.objects.get(student=student).delete()
        if reason == "return_restroom":
            time_out = Record.objects.filter(student = student).order_by('-timestamp')[1].timestamp
            time_out_minutes = time_out.hour * 60 + time_out.minute
            time_back = datetime.now(timezone.utc)
            time_back_minutes = time_back.hour * 60 + time_back.minute
            minutes = time_back_minutes - time_out_minutes
            bathroom = Bathroom.objects.create(student=student, time_out=time_out, time_back=time_back, minutes=minutes)
            bathroom.save()
        return HttpResponseRedirect(reverse("login"))

