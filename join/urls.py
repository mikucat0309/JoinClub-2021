from django.urls import path

from . import views

app_name = 'join'

urlpatterns = [
    path('join', views.join, name="join"),
    path('secret', views.join_secret, name="secret"),
    path('search', views.search, name="search"),
    path('secretSearch', views.secretSearch, name="secretSearch"),
    path('searchForMember', views.searchForMember, name="searchForMember"),
    path('review/<int:id>', views.review, name="review"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('view', views.view, name="view"),
]
