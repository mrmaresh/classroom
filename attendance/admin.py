from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Student, Record, Restroom

class StudentAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("first", "last", "student_id", "period", "id")

class RestroomAdmin (admin.ModelAdmin):
    list_display = ("student", "timestamp_left", "timestamp_return", "time_restroom", "id")



admin.site.register(Student, StudentAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Restroom, RestroomAdmin)


