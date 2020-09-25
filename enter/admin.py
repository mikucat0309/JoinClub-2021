from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Attend, Checkin

class AttendAdmin(ImportExportModelAdmin):
    search_fields = ('name', 'nid',)

class CheckinAdmin(ImportExportModelAdmin):
    search_fields = ('nid', 'status',)

admin.site.register(Attend, AttendAdmin)
admin.site.register(Checkin, CheckinAdmin)

