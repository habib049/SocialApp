from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.template.loader import render_to_string
from rest_framework.generics import ListAPIView
from .serializers import UserListSerializer
from django.db.models import Q
from django.views.generic import UpdateView
from accounts.models import User
from friends.consumers import NotificationConsumer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ProfileUpdateView(UpdateView):
    model = User
    template_name = "profile/profile_update.html"
    context_object_name = "user_profile"
    fields = '__all__'

    def get_object(self, queryset=None):
        return self.request.user.user_profile


class SearchUserList(ListAPIView):
    serializer_class = UserListSerializer

    def list(self, request, *args, **kwargs):
        query = request.GET['query']
        queryset = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )
        html = render_to_string('home/search.html', {'dishes': "dishes"})
        print(html)
        print("This is a type of ", type(html))
        serialize_tmeplate = serializers.serialize('json', html)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'users': serializer.data})
