from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.LoginView.as_view(), name="user_login"),
    path('registration', views.RegistrationView.as_view(), name="user_registration"),
    path('logout', views.LogoutView.as_view(), name="user_logout")

]
