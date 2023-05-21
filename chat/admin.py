from django.contrib import admin
from .models import ChatMessage, ChatRoom


admin.site.register(ChatMessage)
admin.site.register(ChatRoom)