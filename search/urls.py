from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.TopList.as_view(), name="top_search_result"),
    path('top', views.TopList.as_view(), name="top-search-query"),
]
