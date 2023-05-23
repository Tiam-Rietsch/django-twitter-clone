from django.shortcuts import render
from django.db.models import Q
from .models import ChatRoom
from trends.models import Trend



def chat_room_list_view(request):
    chat_rooms = request.user.profile.chatroom_set.all()
    context = {
        'chat_rooms': chat_rooms,
        'topics': Trend.objects.all()
    }
    return render(request, 'pages/chat_room_list.html', context)


def chat_room_view(request, room_name):
    room = ChatRoom.objects.get(name=room_name)
    receiver = room.participants.exclude(user__email=request.user.email)
    return render(request, 'pages/chat_room.html', {'room': room, 'receiver': receiver[0], 'topics': Trend.objects.all()})