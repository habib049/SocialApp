from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from .serializers import UserListSerializer
from django.db.models import Q, Subquery
from django.views.generic import UpdateView, DetailView
from accounts.models import User
from posts.models import Post
from friends.models import Friend
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


class UserProfile(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'home/user_profile.html'

    def get_queryset(self):
        query_set = User.objects.filter(
            slug=self.kwargs.get('slug')
        ).prefetch_related(
            'user_profile', 'user_education'
        )
        return query_set

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        # getting posts
        posts = Post.objects.filter(
            user__slug=self.kwargs.get('slug')
        ).prefetch_related(
            'post_like', 'post_comment', 'post_image'
        )

        # getting mutual friends
        my_friends = Subquery(Friend.objects.filter(
            user=self.request.user
        ).values('friend__username'))

        mutual_friends = Friend.objects.filter(
            friend__username__in=my_friends
        ).values(
            'friend__first_name', 'friend__last_name', 'friend__last_name','friend__user_profile__profile_image'
        )[:9]
        context['mutual_friends'] = mutual_friends
        context['posts'] = posts
        return context
