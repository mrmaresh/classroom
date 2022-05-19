import json
from datetime import datetime, timedelta
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count




# Create your views here.

from .models import Student, Record

def login(request):
    students = []
    time_threshold = datetime.now() - timedelta(hours=1)
    record_query = Record.objects.filter(timestamp__gt=time_threshold).values('student_id').annotate(dcount=Count('student_id'))
    for record in record_query:
        if record['dcount'] % 2 == 1:
            name = Student.objects.get(student_id = record['student_id']).first
            students.append(name)
    return render(request, "login.html",{
        "students": students
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
        if len(Student.objects.filter(student_id=student_id)) == 0:
            messages.add_message(request, messages.INFO, 'Incorrect Student ID.')
            return HttpResponseRedirect(reverse("login"))
        else:
            student = Student.objects.get(student_id=student_id)
            time_threshold = datetime.now() - timedelta(hours=1)
            records = Record.objects.filter(student=student, timestamp__gt=time_threshold).order_by('-timestamp')
            returning = is_returning(records)
            usage = restroom_usage(records)

            return render(request, 'select.html',{
                "student": student,
                "returning": returning,
                "usage": usage
            })



def record(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        reason = request.POST["reason"]
        student = Student.objects.get(student_id=student_id)
        record = Record.objects.create(student=student, reason=reason)
        record.save()
        return HttpResponseRedirect(reverse("login"))

