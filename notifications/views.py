from django.shortcuts import render
from django.views.generic import ListView
from .models import Notification


class NotificationsList(ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'home/notification.html'
    paginate_by = 7

    def get_queryset(self):
        return Notification.objects.filter(
            receiver=self.request.user
        ).order_by(
            '-time_stamp'
        ).select_related(
            'sender',
            'receiver'
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NotificationsList, self).get_context_data(**kwargs)
        unseen = Notification.objects.filter(
            receiver=self.request.user,
            seen=False
        )
        for unseen_notification in unseen:
            unseen_notification.seen = True
            unseen_notification.save()

        context['unseen'] = unseen.count()
        print(context)
        return context
