from django.views.generic import View
from django.http import JsonResponse
from join.models import Member
from enter.models import Attend, Checkin

class ComingsoonData(View):
    def get(self, request):
        Attend_count = Attend.objects.all().count()
        data =  {'Attend_count': Attend_count, }
        return JsonResponse(data)

class JoinclubData(View):
    def get(self, request):
        Checkin_count = Checkin.objects.all().count()
        Member_count = Member.objects.all().count()
        M_count = Member.objects.filter(status='M').count()
        data =  {'Checkin_count': Checkin_count, 'Member_count': Member_count, 'M_count': M_count}
        return JsonResponse(data)

class ReceiveprizeData(View):
    def get(self, request):
        Checkin_count = Checkin.objects.all().count()
        Tix_count = Checkin.objects.filter(status='TIX').count() #已使用票券領獎
        FORM_count = Checkin.objects.filter(status='FORM').count() #已填表單領獎
        MIX_count = Checkin.objects.filter(status='MIX').count() #已填表單加使用票券領獎
        Prize_count = Tix_count + FORM_count + MIX_count
        data =  {'Checkin_count': Checkin_count, 'Prize_count': Prize_count}
        return JsonResponse(data)

class AttendanceData(View):
    def get(self, request):
        Attend_count = Attend.objects.all().count()
        Tix_count = Checkin.objects.filter(status='TIX').count() #已使用票券領獎
        NO_count = Checkin.objects.filter(status='NO').count() #已填表單領獎
        Count = Attend_count - Tix_count - NO_count
        data =  {'Attend_count': Attend_count, 'Count': Count}
        return JsonResponse(data)
