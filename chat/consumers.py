import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime

from .models import ChatMessage, ChatRoom

class ChatConsummer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name   
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        message = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message['message'],
                'author': message['author']
            }
        )


    def send_message(self, event):
        message = event['message']
        chat_room = ChatRoom.objects.get(name=self.scope['url_route']['kwargs']['room_name'])
        time_sent = ''

        if str(event['author']) == str(self.scope['user'].profile):
            print('hey')
            chat_message = ChatMessage.objects.create(
                author=self.scope['user'].profile,
                text=message,
                room=chat_room
            )
            chat_message.save()
            time_sent = chat_message.date_created.strftime('%H:%M')

            self.send(text_data=json.dumps({
                'message': message,
                'sender': event['author'],
                'time_sent': time_sent
            }))
        else:
            self.send(text_data=json.dumps({
                'message': message,
                'sender': event['author'],
                'time_sent': datetime.now().strftime('%H:%M')
            }))
