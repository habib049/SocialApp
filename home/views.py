from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView
from django.urls import reverse_lazy
from posts.models import Post, PostImage


def home_view(request):
    posts = Post.objects.all()
    return render(request, 'home/index.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'home/index.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 5
