from django.http import JsonResponse
from django.db.models import Q
from rest_framework.generics import ListAPIView
from django.views.generic import ListView
from posts.models import Post
from accounts.models import User
from .serializers import UserSerializer, PostSerializer


class UserList(ListView):
    context_object_name = "user_list"
    template_name = 'home/search.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET['q']
        return User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        query = self.request.GET['q']
        context['query'] = query
        return context

