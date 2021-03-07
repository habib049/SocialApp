from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.Contact.as_view(), name='chat_index'),
    path('<str:friend_name>',views.ContactFriendName.as_view(),name="chat_with_friend"),
    path('messages/fetch-messages', views.fetch_messages, name='fetch_messages'),
]
