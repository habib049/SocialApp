from django.db.models import Q, Subquery
from django.views.generic import UpdateView, DetailView
from accounts.models import User
from posts.models import Post
from friends.models import Friend
from notifications.models import Notification
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
            user__slug=self.kwargs.get('slug'),
            friend__username__in=my_friends
        ).values(
            'friend__first_name', 'friend__last_name',
            'friend__last_name', 'friend__user_profile__profile_image',
            'friend__slug'
        )[:9]
        context['requested_user_slug'] = self.kwargs.get('slug')
        context['mutual_friends'] = mutual_friends
        context['posts'] = posts

        # adding notification in database
        sender = self.request.user
        receiver = User.objects.get(
            slug=self.kwargs.get('slug')
        )

        notification = Notification.objects.create(type="profile", sender=sender, receiver=receiver,
                                                   note="viewed your profile")
        notification.save()

        data = {
            'sender': sender.username,
            'receiver': receiver.username,
            'imageUrl': sender.user_profile.profile_image.url,
            'message': "viewed your profile",
            'type': 'profile'
        }

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            str(receiver.username),
            {
                "type": "notify",
                "text": data,
            },
        )

        return context
