from django.contrib import admin
from .models import User, Profile
from tweet.models import Tweet

class TweetInline(admin.StackedInline):
    model = Tweet

class ModelAdmin(admin.ModelAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'username', 'is_staff']
    inlines = [TweetInline]


admin.site.register(User, ModelAdmin)
admin.site.register(Profile)
