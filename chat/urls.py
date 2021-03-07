from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.Contact.as_view(), name='chat_index'),
    path('fectch-messages', views.fetch_messages, name='fetch_messages'),
]
