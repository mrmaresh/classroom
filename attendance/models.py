from django.db import models

# Create your models here.

class Student (models.Model):
    id = models.AutoField(primary_key=True)
    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)
    student_id = models.CharField(max_length=10)
    period = models.CharField(max_length=1)
    exception = models.BooleanField()


class Record (models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name = "student_record")
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=20)


class Bathroom (models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name = "student_bathroom")
    time_out = models.DateTimeField()
    time_back = models.DateTimeField()
    minutes = models.IntegerField()


class Waitlist (models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name = "student_waitlist")


class Schedule (models.Model):
    id = models.AutoField(primary_key=True)
    schedule_name = models.CharField(max_length=20)
    active = models.BooleanField()
    period_0 = models.CharField(max_length=20)
    period_1 = models.CharField(max_length=20)
    period_2 = models.CharField(max_length=20)
    period_3 = models.CharField(max_length=20)
    period_4 = models.CharField(max_length=20)
    period_5 = models.CharField(max_length=20)
    period_6 = models.CharField(max_length=20)
    period_7 = models.CharField(max_length=20)
    period_8 = models.CharField(max_length=20)


class BathroomPass (models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name = "student_bathroom")