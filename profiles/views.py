from django.shortcuts import render
from django.views.generic import UpdateView
from accounts.models import User


class ProfileUpdateView(UpdateView):
    model = User
    template_name = "profile/profile_update.html"
    context_object_name = "user_profile"
    fields = '__all__'

    def get_object(self, queryset=None):
        return self.request.user.user_profile

