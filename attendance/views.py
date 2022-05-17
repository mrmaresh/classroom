import json
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

from .models import Student, Record

def login(request):
    return render(request, "login.html")

def is_returning(records):
    if len(records) > 0:
        if records[0].reason == "use_restroom" and records[0].timestamp.hour + 1 >= datetime.now().hour and records[0].timestamp.day == datetime.now().day:
            return True
        else:
            return False
    else:
        return False

def restroom_usage(records):
    pass
    usage = []
    for n in range(len(records)):
        time = records[n].timestamp
        minutes = time.hour * 60 + time.minute
        if n % 2 == 0:
            returned = time.time
            returned_minutes = minutes
        else:
            left = time.time
            left_minutes = minutes
            date = records[n].timestamp.date
            total = returned_minutes - left_minutes
            entry = {'date':date, 'left':left, 'returned':returned, 'total':total}
            usage.append(entry)
    return usage

def select(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        if len(Student.objects.filter(student_id=student_id)) == 0:
            messages.add_message(request, messages.INFO, 'Incorrect Student ID.')
            return HttpResponseRedirect(reverse("login"))
        else:
            student = Student.objects.get(student_id=student_id)
            records = Record.objects.filter(student=student).order_by('-timestamp')
            returning = is_returning(records)
            usage = restroom_usage(records)

            return render(request, 'select.html',{
                "student": student,
                "returning": returning,
                "time": datetime.now().time
            })



def record(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        reason = request.POST["reason"]
        student = Student.objects.get(student_id=student_id)
        record = Record.objects.create(student=student, reason=reason)
        record.save()
        return HttpResponseRedirect(reverse("login"))

