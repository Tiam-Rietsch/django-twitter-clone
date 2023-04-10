from django.db import models
from users.models import Profile

class Notification(models.Model):
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_notifications')
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='sent_notifications')
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=200)
    body = models.TextField()
    viewed = models.BooleanField(default=False, null=True)

    
    def __str__(self):
        return '@' + self.sender.user.username + ' to @' + self.receiver.user.username + ':  ' + self.title