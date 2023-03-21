from django.contrib import admin
from .models import Tweet, TweetLike, Repost

admin.site.register(TweetLike)
admin.site.register(Repost)
admin.site.register(Tweet)
