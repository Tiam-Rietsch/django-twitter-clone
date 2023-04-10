from django.urls import path 

from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('create-tweet/', views.create_tweet_view, name='create-tweet'),
    path('tweet-detail/<int:pk>/', views.tweet_detail_view, name='tweet-detail'),

    path('retweet/', views.retweet_view, name='retweet'),

    path('get-like-count/', views.get_like_count, name='get-like-count'),
    path('like-action/', views.like_action, name='like-action'),

    path('get-repost-count/', views.get_repost_count, name='get-repost-count'),
    path('refresh-tweet-count/', views.refresh_tweet_count, name='refresh-tweet-count'),
    path('check-tweet-existence/', views.check_tweet_existence, name='check-tweet-existence'),

    path('search-topic/', views.android_search_page_view, name='search-topic'),
]