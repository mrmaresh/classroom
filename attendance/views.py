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


def select(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        if len(Student.objects.filter(student_id=student_id)) == 0:
            messages.add_message(request, messages.INFO, 'Incorrect Student ID.')
            return HttpResponseRedirect(reverse("login"))
        else:
            student = Student.objects.get(student_id=student_id)
            records = Record.objects.filter(student=student).order_by('-timestamp')
            if len(records) > 0:
                if records.first().reason == "use_restroom":
                    returning = True
                else:
                    returning = False
            else:
                returning = False
            return render(request, 'select.html',{
                "student": student,
                "returning": returning,
                "time": datetime.now()
            })


def record(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        reason = request.POST["reason"]
        student = Student.objects.get(student_id=student_id)
        record = Record.objects.create(student=student, reason=reason)
        record.save()
        return HttpResponseRedirect(reverse("login"))

