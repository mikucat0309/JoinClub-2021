from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('comingsoondata', views.ComingsoonData.as_view(), name="comingsoondata"),
    path('joinclubdata', views.JoinclubData.as_view(), name="joinclubdata"),
    path('receiveprizedata', views.ReceiveprizeData.as_view(), name="receiveprizedata"),
    path('attendancedata', views.AttendanceData.as_view(), name="attendancedata"),
]