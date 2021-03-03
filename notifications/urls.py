from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationsList.as_view(), name="notification_list")
]
