from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from posts.models import Post, PostImage


def home_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('accounts:user_login'))

    posts = Post.objects.all()
    #
    # post_images = list()
    #
    # for post in posts:
    #     post_images.append(PostImage.objects.filter(post=post))
    #

    return render(request, 'home/index.html', {'posts': posts})
