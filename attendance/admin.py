from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Student, Record, Bathroom, Waitlist

class StudentAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("first", "last", "student_id", "period", "exception", "id")

class RecordAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("student_id", "timestamp", "reason", "id")

class BathroomAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("student_id", "time_out", "time_back", "minutes", "id")

class WaitlistAdmin (admin.ModelAdmin):
    list_display = ("student_id", "id")



admin.site.register(Student, StudentAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Bathroom, BathroomAdmin)
admin.site.register(Waitlist, WaitlistAdmin)


