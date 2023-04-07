from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class Tweet(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField()
    attachement = models.ImageField(blank=True, null=True, upload_to='attachements')
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return self.body[:30] + '...'
    
    class Meta:
        ordering = ['-date_created']
    

class TweetLike(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Repost(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    source_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='sources', null=True)
    repost_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='reposts', null=True)

