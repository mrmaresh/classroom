from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Student, Record, Bathroom, Waitlist, Schedule, AttendanceRecord, Incident

class StudentAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("first", "last", "student_id", "period", "exception", "augPass", "sepPass", "octPass", "novPass", "decPass", "janPass", "febPass", "marPass", "aprPass", "mayPass", "junPass", "julPass", "responses", "absent", "id")

class RecordAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("student_id", "timestamp", "reason", "id")

class AttendanceRecordAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("student_id", "timestamp", "excused", "reason", "id")

class IncidentAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("student_id", "timestamp", "reason", "referral_url", "id")

class BathroomAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("student_id", "time_out", "time_back", "minutes", "id")

class WaitlistAdmin (admin.ModelAdmin):
    list_display = ("student_id", "id")

class ScheduleAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("schedule_name", "active", "period_0", "period_1", "period_2", "period_3", "period_4", "period_5", "period_6", "period_7", "period_8",)



admin.site.register(Student, StudentAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(Bathroom, BathroomAdmin)
admin.site.register(Waitlist, WaitlistAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Incident, IncidentAdmin)


