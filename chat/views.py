from django.shortcuts import render

def chat_room_list_view(request):
    chat_rooms = request.user.profile.chatroom_set.all()
    context = {'chat_rooms': chat_rooms}
    return render(request, 'pages/chat_room_list.html', context)


def chat_room_view(request, room_name):
    return render(request, 'pages/chat_room.html')