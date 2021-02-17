from django.urls import path
from . import views

app_name = 'friend'

urlpatterns = [
    path('send-request', views.view, name="send_request")
]
