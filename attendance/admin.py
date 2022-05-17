from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Student, Record

class StudentAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display = ("first", "last", "student_id", "period", "id")


admin.site.register(Student, StudentAdmin)
admin.site.register(Record, RecordAdmin)



