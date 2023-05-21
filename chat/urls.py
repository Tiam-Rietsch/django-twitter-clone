from django.urls import path 
from . import views


urlpatterns = [
    path('chat/', views.chat_room_list_view, name='room_list'),
    path('chat/<str:room_name>/', views.chat_room_view, name='chat_room'),
]