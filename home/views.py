from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView
from django.urls import reverse_lazy
from posts.models import Post
from accounts.models import User
from friends.models import Friend


def home_view(request):
    posts = Post.objects.all()
    return render(request, 'home/index.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'home/index.html'
    queryset = Post.objects.all().prefetch_related('post_comment', 'post_image', 'post_like')
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        friends = Friend.objects.filter(user=self.request.user, status="requested").select_related('user','friend')
        context['friends'] = friends[:5]
        context['requested_count'] = friends.count()
        return context


class RequestFriendList(ListView):
    model = Friend
    context_object_name = 'friends'
    paginate_by = 5

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user, status='requested')
