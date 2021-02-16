from django.http import JsonResponse
from django.db.models import Q
from rest_framework.generics import ListAPIView
from django.views.generic import ListView
from posts.models import Post
from accounts.models import User
from .serializers import UserSerializer, PostSerializer


class TopList(ListView):
    context_object_name = "user_list"
    template_name = 'home/search.html'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET['q']
        return User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )

    def get_context_data(self, **kwargs):
        print(self.request)
        context = super(TopList, self).get_context_data(**kwargs)
        query = self.request.GET['q']
        context['query'] = query
        context['post_list'] = Post.objects.filter(
            Q(title__icontains=query) |
            Q(sub_title__icontains=query) |
            Q(content__icontains=query)
        )
        return context


class TopList1(ListAPIView):

    def list(self, request, *args, **kwargs):
        print(request.GET)
        query = request.GET('q')
        queryset = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )
        serializer_user_data = UserSerializer(queryset)

        queryset = Post.objects.filter(
            Q(title__icontains=query) |
            Q(sub_title__icontains=query) |
            Q(content__icontains=query)
        )
        serializer_posts_data = PostSerializer(queryset)
        return JsonResponse({'users': serializer_user_data.data, 'posts': serializer_posts_data.data})
