from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.UserList.as_view(), name="user_search_result"),
    path('ajax/<str:query>', views.SearchUserList.as_view(), name="ajax_search_result"),
    path('path/<str:query>', views.check, name="check")
]
