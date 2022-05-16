from django.db import models

# Create your models here.

class Student (models.Model):
    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)
    student_id = models.CharField(max_length=10)
    period = models.CharField(max_length=1)


class Record (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name = "student")
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=20)