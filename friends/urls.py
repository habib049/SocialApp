from django.urls import path
from . import views

app_name = 'friend'

urlpatterns = [
    path('', views.FriendList.as_view(), name="user_friends"),
    path('mutual-friend/<slug:slug>', views.MutualFriendList.as_view(), name='mutual_friend_list'),
    path('send-friend-request', views.send_friend_request, name="send_friend_request"),
    path('accept-friend-request', views.accept_friend_request, name='accept_friend_request'),
]
