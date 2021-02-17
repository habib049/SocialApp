from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.UserList.as_view(), name="user_search_result"),
]
