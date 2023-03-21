from django.urls import path 

from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('create-tweet/', views.create_tweet_view, name='create-tweet'),
    path('tweet-detail/<int:pk>/', views.tweet_detail_view, name='tweet-detail'),
]