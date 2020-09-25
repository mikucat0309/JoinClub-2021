from import_export import resources
from .models import Person

class MemberResource(resources.ModelResource):
    class Meta:
        model = Member

class AttendResource(resources.ModelResource):
    class Meta:
        model = Attend
