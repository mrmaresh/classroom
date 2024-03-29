import json
import time
import random
from datetime import datetime, timedelta, timezone, time, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count


# Create your views here.

from .models import Student, Record, Bathroom, Waitlist, Schedule, AttendanceRecord, Incident

# ISSUE:  what period is detected during passing period?
# Create a function that sets the default schedule and have it automatically run every morning prior to school
# Create a function that resets the waitlist every change of period automatically
# Create a student dashboard which displays the joke of the day, homework, reminders, birthdays


@csrf_exempt
@login_required
def attendance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        reason = data.get("reason")
        excused = data.get("excused")
        student_id = data.get("student_id")
        student = Student.objects.get(student_id=student_id)
        record = AttendanceRecord.objects.create(student=student, reason=reason, excused=excused)
        record.save()
        return JsonResponse({"message": reason, "excused": excused, "student_id": student_id})





@csrf_exempt
@login_required
def resetWaitlist(request):
    if request.method == "POST":
        Waitlist.objects.all().delete()
        return JsonResponse({"message": "Waitlist has been reset"})


@csrf_exempt
@login_required
def resetAbsences(request):
    if request.method == "POST":
        for record in Student.objects.all():
            record.absent = False
            record.save()
        return JsonResponse({"message": "Waitlist has been reset"})

@csrf_exempt
@login_required
def recordAbsence(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get("student_id")
        student = Student.objects.get(student_id=student_id)
        student.absent = True
        student.save()
        return JsonResponse({"message": "student data has been updated"})


@csrf_exempt
@login_required
def unexcused(request, student_id):
    if request.method == "GET":
        student = Student.objects.get(student_id=student_id)
        records = AttendanceRecord.objects.filter(student=student, excused=False)
        return JsonResponse({"numTardies": len(records)})

@csrf_exempt
@login_required
def checkNewPeriod(request):
    if request.method == "GET":
        period = get_current_period()
        return JsonResponse({"currentPeriod": period[0]})

#This function will GET a random student within a period that is not absent or POST that a student has responded.
@csrf_exempt
@login_required
def randomStudent(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get("student_id")
        student = Student.objects.get(student_id=student_id)
        student.responses = student.responses + 1
        student.save()
        return JsonResponse({"message": "student data has been updated"})

    if request.method == "GET":
        getPeriod = get_current_period()
        period_num = getPeriod[0][-1]
        min_person = Student.objects.filter(period=period_num, absent = False).order_by('responses').first()
        min_responses = min_person.responses + 1
        random_people = Student.objects.filter(period=period_num, responses__lte=min_responses, absent = False)
        num = len(random_people)
        random_student = random_people[random.randint(0,num - 1)]
        first = random_student.first
        last = random_student.last
        student_id = random_student.student_id
        name = first + " " + last
        return JsonResponse({
            "responses": min_responses,
            "first": first,
            "last": last,
            "name": name,
            "num": num,
            "student_id": student_id
        })



# This function detects what is the current period
def get_current_period():
    now = datetime.now()
    is_max = False
    period = ['period_0', 'period_1', 'period_2', 'period_3', 'period_4', 'period_5', 'period_6', 'period_7', 'period_8']
    for i in range(9):
        then = datetime.strptime(getattr(Schedule.objects.get(active = True), period[i]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)  - timedelta(minutes=7)
        max = datetime.strptime(getattr(Schedule.objects.get(active = True), period[8]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)  - timedelta(minutes=7)
        if now < then:
            if then == max:
                is_max = True
            return [period[i-1], period[i], is_max]
    return ['period_0', 'period_1', is_max]


# This displays a default page for all who are not logged in
def restricted(request):
    return render(request, "restricted.html")


def students_using_restroom():
    period = get_current_period()
    start = datetime.strptime(getattr(Schedule.objects.get(active = True), period[0]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year) - timedelta(minutes=7)
    finish = datetime.strptime(getattr(Schedule.objects.get(active = True), period[1]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
    # This is a list of all the students currently using the restroom
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
    return students




# This is the student login page
@login_required(login_url='restricted')
def login(request):
    period = get_current_period()
    start = datetime.strptime(getattr(Schedule.objects.get(active = True), period[0]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year) - timedelta(minutes=7)
    finish = datetime.strptime(getattr(Schedule.objects.get(active = True), period[1]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
    finish_time = finish - timedelta(minutes=7)
    if period[2] == True:
        finish_time = finish
    start_time = start + timedelta(minutes=7)
    # This is a list of all the students currently using the restroom
    students = students_using_restroom()
    # This checks if someone is using the restroom
    if len(students) > 0:
        in_use = True
    else:
        in_use = False

    # This checks if someone is waiting for the restroom
    if len(Waitlist.objects.all()) > 0:
        waiting = True
    else:
        waiting = False


    return render(request, "login.html",{
        "students": students,
        "in_use": in_use,
        "waitlist": Waitlist.objects.all(),
        "waiting": waiting,
        "records": Record.objects.filter(timestamp__range = [start,finish]),
        "period": get_current_period()[0][-1],
        "start": start,
        "finish": finish,
        "schedule": Schedule.objects.get(active = True).schedule_name,
        "start_time": start_time.time,
        "finish_time": finish_time.time
    })


@login_required
def choice(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        in_use = request.POST["in_use"]
        if len(Student.objects.filter(student_id=student_id)) == 0:
            messages.add_message(request, messages.INFO, 'Incorrect Student ID.')
            return HttpResponseRedirect(reverse("login"))
        else:
            return render(request, 'choice.html',{
                "student_id": student_id,
                "in_use": in_use
            })


def is_returning(records):
    if len(records) > 0:
        if records[0].reason == "use_restroom":
            return True
        else:
            return False
    else:
        return False

def numPass(student):
    month = datetime.now().month
    list = ["janPass", "febPass", "marPass", "aprPass", "mayPass", "junPass", "julPass", "augPass", "sepPass", "octPass", "novPass", "decPass"]
    if getattr(student, list[month - 1]) == True:
        return 1
    else:
        return 0


def usePass(student):
    month = datetime.now().month
    list = ["janPass", "febPass", "marPass", "aprPass", "mayPass", "junPass", "julPass", "augPass", "sepPass", "octPass", "novPass", "decPass"]
    value = list[month - 1]
    if value == "janPass":
        student.janPass = False
    if value == "febPass":
        student.febPass = False
    if value == "marPass":
        student.marPass = False
    if value == "aprPass":
        student.aprPass = False
    if value == "mayPass":
        student.mayPass = False
    if value == "junPass":
        student.junPass = False
    if value == "julPass":
        student.julPass = False
    if value == "augPass":
        student.augPass = False
    if value == "sepPass":
        student.sepPass = False
    if value == "octPass":
        student.octPass = False
    if value == "novPass":
        student.novPass = False
    if value == "decPass":
        student.decPass = False

    student.save()



@login_required
def select(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        in_use = request.POST["in_use"]
        student = Student.objects.get(student_id=student_id)

        period = get_current_period()
        start = datetime.strptime(getattr(Schedule.objects.get(active = True), period[0]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year) - timedelta(minutes=7)
        finish = datetime.strptime(getattr(Schedule.objects.get(active = True), period[1]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
        start_time = start + timedelta(minutes=7)
        moreThanHour = datetime.now() - start_time > timedelta(minutes = 60)

        records = Record.objects.filter(student=student, timestamp__range = [start,finish]).order_by('-timestamp')
        returning = is_returning(records)
        return render(request, 'select.html',{
            "records": records,
            "moreThanHour": moreThanHour,
            "numPass": numPass(student),
            "student": student,
            "returning": returning,
            "usage": Bathroom.objects.filter(student=student).order_by('-time_out'),
            "in_use": in_use
        })


@login_required
def attendancePage(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        student = Student.objects.get(student_id=student_id)
        records = AttendanceRecord.objects.filter(student=student, excused=False).order_by('-timestamp')
        return render(request, 'attendance2.html',{
            "student": student,
            "numTardies": len(records),
            "records": records
        })


@login_required
def incidentPage(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        student = Student.objects.get(student_id=student_id)
        return render(request, 'incident.html',{
            "student": student,
            "records": Incident.objects.filter(student=student).order_by('-timestamp'),
            "recordsLength": len(Incident.objects.filter(student=student))
        })

@login_required
def incident(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        reason = request.POST["reason"]
        if reason == "Cell Phone Issue":
            Reason = "Cell+phone+disruption+in+class"
        elif reason == "Earbud Issue":
            Reason = "Repeated+or+defiant+earbud/headphone+use"
        elif reason == "Dress Code Violation":
            Reason = "Dress+Code"
        student = Student.objects.get(student_id=student_id)
        referral_name = "entry.1761415926=" + student.last + ",+" + student.first
        referral_teacher = "&entry.53902594=Maresh/D26"
        referral_id = "&entry.560109928=" + student_id
        referral_grade = "&entry.174482171=" + student.grade
        referral_period = "&entry.751509150=" + student.period
        referral_reason = "&entry.1334361462=" + Reason
        referral_intervention = "&entry.1608002152=Warning/Counsel"
        incidents = Incident.objects.filter(reason=reason, student=student)
        num = len(incidents)
        circumstance = "This+issue+has+already+happened+" + str(num)
        if num == 1:
            circumstance = circumstance + "time+before+on+the+following+date:+"
        else:
            circumstance = circumstance + "+times+before+on+the+following+dates:+"
        for record in incidents:
            circumstance = circumstance + record.timestamp.strftime("%m/%d/%Y") + ",+"
        referral_circumstances = "&entry.656152471=" + circumstance
        referral_choice = "&entry.674564845=Sending+Student"
        now = datetime.now()
        referral_date = "&entry.59733697_year=" + now.strftime("%Y") + "&entry.59733697_month=" + now.strftime("%m") + "&entry.59733697_day=" + now.strftime("%d")
        referral_time = "&entry.462999847_hour=" + now.strftime("%H") + "&entry.462999847_minute=" + now.strftime("%M")
        referral_url = "https://docs.google.com/forms/d/e/1FAIpQLSdndO7Z1TXeb0igq3lY7x6mX29Ezek00fBUwk05zNrHeXhqHg/viewform?"
        referral_url = referral_url + referral_name  + referral_teacher + referral_id + referral_grade + referral_period + referral_reason + referral_intervention + referral_circumstances + referral_choice + referral_date + referral_time

        record = Incident.objects.create(student=student, reason = reason, referral_url=referral_url)
        record.save()

        return HttpResponseRedirect(reverse('login'))


def waitlist(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        student = Student.objects.get(student_id = student_id)
        if len(Waitlist.objects.filter(student=student)) == 0:
            entry = Waitlist.objects.create(student = student)
            entry.save()
        return HttpResponseRedirect(reverse("login"))


@login_required
def dashboard(request):

    period = get_current_period()
    start = datetime.strptime(getattr(Schedule.objects.get(active = True), period[0]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)  - timedelta(minutes=7)
    finish = datetime.strptime(getattr(Schedule.objects.get(active = True), period[1]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)

    finish_time = finish - timedelta(minutes=7)
    if period[2] == True:
        finish_time = finish
    start_time = start + timedelta(minutes=7)
    startdate = datetime.today()-timedelta(hours=8)
    records = Bathroom.objects.filter(time_out__gt = startdate).order_by('-time_out')
    tardyRecords = AttendanceRecord.objects.filter(timestamp__gt = startdate).order_by('-timestamp')
    incidentRecords = Incident.objects.filter(timestamp__gt = startdate).order_by('-timestamp')
    numUnexTardies = []
    numTardies = []
    numBath = []
    numPhone = []
    numEarbud = []
    numDressCode = []
    for student in Student.objects.all():
        numUnexTardies.append((student.first, student.last, student.student_id, len(AttendanceRecord.objects.filter(student=student, excused=False))))
        numTardies.append((student.first, student.last, student.student_id, len(AttendanceRecord.objects.filter(student=student))))
        numBath.append((student.first, student.last, student.student_id, len(Bathroom.objects.filter(student=student))))
        numPhone.append((student.first, student.last, student.student_id, len(Incident.objects.filter(student=student, reason = "Cell Phone Issue"))))
        numEarbud.append((student.first, student.last, student.student_id, len(Incident.objects.filter(student=student, reason = "Earbud Issue"))))
        numDressCode.append((student.first, student.last, student.student_id, len(Incident.objects.filter(student=student, reason = "Dress Code Violation"))))

    numUnexTardies = sorted(numUnexTardies, key=lambda i:i[3], reverse=True)
    numTardies = sorted(numTardies, key=lambda i:i[3], reverse=True)
    numBath = sorted(numBath, key=lambda i:i[3], reverse=True)
    numPhone = sorted(numPhone, key=lambda i:i[3], reverse=True)
    numEarbud = sorted(numEarbud, key=lambda i:i[3], reverse=True)
    numDressCode = sorted(numDressCode, key=lambda i:i[3], reverse=True)

    currentWaitlist = []
    for record in Waitlist.objects.all():
        currentWaitlist.append(record.student.first)

    bathDate = {}
    for record in Bathroom.objects.all():
        bathDate[record] = record.time_out.strftime("%m-%d-%Y  %H:%M:%S")

    tardyDate = {}
    for record in AttendanceRecord.objects.all():
        tardyDate[record] = record.timestamp.strftime("%m-%d-%Y  %H:%M:%S")

    incidentDate = {}
    for record in Incident.objects.all():
        incidentDate[record] = record.timestamp.strftime("%m-%d-%Y  %H:%M:%S")


    return render(request, 'dashboard.html',{
        "incidentRecords": incidentRecords,
        "tardyRecords": tardyRecords,
        "numUnexTardies": numUnexTardies[0:5],
        "numTardies": numTardies[0:5],
        "numBath": numBath[0:5],
        "numPhone": numPhone[0:5],
        "numEarbud": numEarbud[0:5],
        "numDressCode": numDressCode[0:5],
        "tardies": AttendanceRecord.objects.all(),
        "bathroom": Bathroom.objects.all(),
        "timeSpent":datetime.now() - start_time > timedelta(minutes = 60),
        "waitlist": currentWaitlist,
        "records": records,
        "startdate":startdate.date,
        "hour": datetime.now().hour,
        "minute": datetime.now().minute,
        "schedule": Schedule.objects.get(active=True).schedule_name,
        "recordz": Record.objects.filter(timestamp__range = [start,finish]),
        "period": get_current_period(),
        "period_number": get_current_period()[0][-1],
        "start": start_time.time,
        "finish": finish_time.time,
        "using_restroom": students_using_restroom(),
        "options": Schedule.objects.all(),
        "bathDate": bathDate,
        "tardyDate": tardyDate,
        "incidentDate": incidentDate
    })


def schedule(request):
    if request.method == "POST":
        active = Schedule.objects.get(active = True)
        active.active = False
        active.save()
        schedule = str(request.POST["schedule"])
        change = Schedule.objects.get(schedule_name = schedule)
        change.active = True
        change.save()

        return HttpResponseRedirect(reverse("dashboard"))




def record(request):
    if request.method == "POST":
        student_id = request.POST["student_id"]
        reason = request.POST["reason"]
        student = Student.objects.get(student_id=student_id)
        record = Record.objects.create(student=student, reason=reason)

        period = get_current_period()
        start = datetime.strptime(getattr(Schedule.objects.get(active = True), period[0]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year) - timedelta(minutes=7)
        finish = datetime.strptime(getattr(Schedule.objects.get(active = True), period[1]), '%H:%M:%S').replace(month = datetime.now().month, day = datetime.now().day, year=datetime.now().year)
        start_time = start + timedelta(minutes=7)
        moreThanHour = datetime.now() - start_time > timedelta(minutes = 60)

        if numPass(student) == 1 and student.exception == False and moreThanHour == False:
            usePass(student)
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

