from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField('users.Profile')

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    author = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now())


    def __str__(self):
        return f'{self.author} : {self.text[:50]} | {self.date_created}'