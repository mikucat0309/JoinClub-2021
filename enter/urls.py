from django.urls import path

from . import views

app_name = 'enter'

urlpatterns = [
    path('attend', views.attend, name="attend"),
    path('search', views.search, name="search"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('checkin', views.checkin, name="checkin"),
    path('prize/<str:nid>', views.prize, name="prize"),
]