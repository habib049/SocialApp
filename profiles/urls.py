from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('update', views.ProfileUpdateView.as_view(), name="update_profile"),
    path('<slug:slug>', views.UserProfile.as_view(), name="user_profile")

]
