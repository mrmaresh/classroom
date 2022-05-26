import json
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count




# Create your views here.

from .models import Student, Record, Bathroom, Waitlist


def login(request):
    students = []
    time_threshold = datetime.now() - timedelta(hours=2)
    record_query = Record.objects.filter(timestamp__gt=time_threshold).values('student_id').annotate(dcount=Count('student_id'))

    if len(record_query) > 0:
        for record in record_query:
            if record['dcount'] % 2 == 1:
                student = Student.objects.get(pk=record['student_id'])
                records = Record.objects.filter(student=student, timestamp__gt=time_threshold).order_by('-timestamp')
                if records[0].reason == "use_restroom":
                    name = Student.objects.get(student_id = student.student_id).first
                    students.append(name)

    if len(students) > 0:
        in_use = True
    else:
        in_use = False

    if len(Waitlist.objects.all()) > 0:
        waiting = True
    else:
        waiting = False

    return render(request, "login.html",{
        "students": students,
        "records": record_query,
        "in_use": in_use,
        "waitlist": Waitlist.objects.all(),
        "waiting": waiting
    })




def is_returning(records):
    if len(records) > 0:
        if records[0].reason == "use_restroom":
            return True
        else:
            return False
    else:
        return False

def restroom_usage(recordz):

    records = list(recordz)
    usage = []
    if not len(records) % 2 == 0:
        time = records[0].timestamp
        date = time.date
        left = time
        returned = ""
        total = ""
        entry = {'date':date, 'left':left, 'returned':returned, 'total':total}
        usage.append(entry)
        records.pop(0)

    for n in range(len(records)):
        time = records[n].timestamp
        minutes = time.hour * 60 + time.minute
        if n % 2 == 0:
            returned = time
            returned_minutes = minutes
        else:
            left = time
            left_minutes = minutes
            date = time.date
            total = returned_minutes - left_minutes
            entry = {'date':date, 'left':left, 'returned':returned, 'total':total}
            usage.append(entry)
    return usage


def select(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        in_use = request.POST["in_use"]
        if len(Student.objects.filter(student_id=student_id)) == 0:
            messages.add_message(request, messages.INFO, 'Incorrect Student ID.')
            return HttpResponseRedirect(reverse("login"))
        else:
            student = Student.objects.get(student_id=student_id)
            time_threshold = datetime.now() - timedelta(hours=1)
            records = Record.objects.filter(student=student, timestamp__gt=time_threshold).order_by('-timestamp')
            recordz = Record.objects.filter(student=student).order_by('-timestamp')
            returning = is_returning(records)
            usage = restroom_usage(recordz)


            return render(request, 'select.html',{
                "student": student,
                "returning": returning,
                "usage": usage,
                "in_use": in_use
            })

def waitlist(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        student = Student.objects.get(student_id = student_id)
        entry = Waitlist.objects.create(student = student)
        entry.save()
        return HttpResponseRedirect(reverse("login"))

def reset(request):
    if request.method == "POST":
        Waitlist.objects.all().delete()
        return HttpResponseRedirect(reverse("dashboard"))

def dashboard(request):
    startdate = datetime.today()-timedelta(hours=8)
    enddate = startdate + timedelta(days=1)
    records = Bathroom.objects.filter(time_out__gt = startdate).order_by('-time_out')
    return render(request, 'dashboard.html',{
        "waitlist": Waitlist.objects.all(),
        "records": records,
        "startdate":startdate.date,
        "hour": datetime.now().hour,
        "minute": datetime.now().minute
    })

def record(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        reason = request.POST["reason"]
        student = Student.objects.get(student_id=student_id)
        record = Record.objects.create(student=student, reason=reason)
        record.save()
        if reason == "use_restroom":
            if student in wait_list:
                wait_list.remove(student)
        if reason == "return_restroom":
            time_out = Record.objects.filter(student = student).order_by('-timestamp')[1].timestamp
            time_out_minutes = time_out.hour * 60 + time_out.minute
            time_back = datetime.now(timezone.utc)
            time_back_minutes = time_back.hour * 60 + time_back.minute
            minutes = time_back_minutes - time_out_minutes
            bathroom = Bathroom.objects.create(student=student, time_out=time_out, time_back=time_back, minutes=minutes)
            bathroom.save()

        return HttpResponseRedirect(reverse("login"))

