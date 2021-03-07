from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    # path('', views.UserList.as_view(), name="user_search_result"),
    path('<str:query>', views.search_user_profiles, name="ajax_search_result"),
    # path('temp/temp/<str:query>', views.check, name="check")
]
