from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.ProfileUpdateView.as_view(), name="update_profile"),
    path('search-profile', views.SearchUserList.as_view(), name="search_profile"),
    path('search', TemplateView.as_view(template_name='home/search.html'), name="render_search_tempalte"),
]
