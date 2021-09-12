from django.urls import path

from . import views

app_name = 'chart'

urlpatterns = [
    path('joinclub', views.joinclub, name="joinclub"),
    path('receiveprize', views.receiveprize, name="receiveprize"),
    path('attendance', views.attendance, name="attendance"),
    path('export_all', views.export_all, name="export_all"),
    path('export_NP', views.export_NP, name="export_NP"),
    path('export_M', views.export_M, name="export_M"),
    path('export_secret', views.export_secret, name="export_secret"),
]
