from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('',views.ProfileUpdateView.as_view(),name="update_profile")
]
