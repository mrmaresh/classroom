from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Student, Record, Bathroom

class StudentAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("first", "last", "student_id", "period", "exception", "id")

class RecordAdmin (admin.ModelAdmin):
    list_display = ("student_id", "timestamp", "reason", "id")

class BathroomAdmin (admin.ModelAdmin):
    list_display = ("student_id", "time_out", "time_back", "minutes", "id")



admin.site.register(Student, StudentAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Bathroom, BathroomAdmin)


