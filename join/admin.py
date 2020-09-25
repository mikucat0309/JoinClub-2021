from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Member

class MemberAdmin(ImportExportModelAdmin):
    search_fields = ('nid',)

admin.site.register(Member, MemberAdmin)

