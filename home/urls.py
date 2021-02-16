from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.PostListView.as_view(),name="home")
]
