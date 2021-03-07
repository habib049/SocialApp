from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from accounts.models import User
from .serializers import UserSerializer


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


class SearchUserList(ListAPIView):
    queryset = User.objects.all()

    def get_queryset(self):
        print(self.request.query_params)

        query = self.request.query_params.get('q')

        return User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)

        query = self.request.query_params.get('q')
        # append serializer's data with some additional value
        response_list = serializer.data
        # for changing the url
        response_list.append({'query': query})
        return Response(response_list)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def check(request,query ):
    if request.is_ajax():
        print("\n\ncalled\n\n")
        html = render_to_string('home/search.html', {'dishes': "dishes"})
        return HttpResponse(html)
