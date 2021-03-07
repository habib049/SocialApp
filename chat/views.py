from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from accounts.models import User
from .models import Message, Room
from .serializers import MessageSerializer


class Contact(ListView):
    model = Message
    paginate_by = 10
    context_object_name = 'contacts'
    template_name = 'home/chat.html'

    def get_queryset(self):
        query = Room.objects.filter(
            Q(user=self.request.user) | Q(friend=self.request.user)
        ).order_by(
            'timestamp'
        ).prefetch_related(
            Prefetch('messages', queryset=Message.objects.order_by(
                'timestamp'
            ))
        )
        return query


def fetch_messages(request):
    if request.is_ajax() and request.method == 'POST':
        sender = request.user
        receiver_name = request.POST.get('friend_name')
        receiver = User.objects.get(username=receiver_name)

        fetched_messages = Message.objects.filter(
            Q(sender=sender, receiver=receiver) |
            Q(sender=receiver, receiver=sender)
        ).order_by(
            'timestamp'
        )

        paginator = Paginator(fetched_messages, 10)
        # for getting last page
        last_page = paginator.num_pages

        # if page is not specified we fetch last page
        page = request.POST.get('page', last_page)

        try:
            fetched_messages = paginator.page(page)
        except PageNotAnInteger:
            fetched_messages = paginator.page(last_page)
        except EmptyPage:
            fetched_messages = paginator.page(paginator.num_pages)

        data = {
            'last_page': last_page
        }

        # serializing data
        serialized_messages = MessageSerializer(fetched_messages, many=True)
        return JsonResponse({
            'messages': serialized_messages.data,
            'page_data': data,
            'user': request.user.username,
            'friend': request.POST.get('friend_name'),
        })
