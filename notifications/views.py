from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification
from trends.models import Trend 
from django.db.models import Q


# Create your views here.
def notification_page_view(request, username):
    notifications = Notification.objects.filter(receiver__user=request.user)
    for notice in notifications.filter(viewed=False):
        notice.viewed=True
        notice.save()

    topics = Trend.objects.all()
    return render(request, 'pages/notifications_page.html', {'notifications': notifications, 'topics': topics})


def get_unviewed_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(Q(receiver__user=request.user) & Q(viewed=False))
        return JsonResponse({'count': notifications.count()})
    else:
        return JsonResponse({'count': 0})
