from django.urls import path 
from . import views

urlpatterns = [
    path('reply-tweet/<int:tweet_id>/', views.tweet_reply_view, name='reply-tweet'),
]