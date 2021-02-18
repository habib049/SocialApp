from django.urls import path
from . import views

app_name = 'friend'

urlpatterns = [
    path('', views.FriendList.as_view(), name="user_friends"),
    path('friend-list', views.FriendListApiView.as_view(), name="friend_list"),
    path('requested-friend-list', views.RequestedListApiView.as_view(), name="requested_friend_list"),
    path('send-friend-request', views.send_friend_request, name="send_friend_request")
]
