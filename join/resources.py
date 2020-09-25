from import_export import resources
from .models import Attend

class AttendResource(resources.ModelResource):
    class Meta:
        model = Attend
