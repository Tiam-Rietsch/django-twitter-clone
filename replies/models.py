from django.db import models
from django.contrib.auth import get_user_model
from tweet.models import Tweet

class Reply(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    attachement = models.ImageField(upload_to='atachements/')

    def __str__(self):
        return self.body[:50]
    
    class Meta:
        verbose_name = 'replie'