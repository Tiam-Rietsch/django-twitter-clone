from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from .forms import TweetCreationForm
from .models import Tweet, TweetLike
from replies.models import Reply

def home_page_view(request):
    tweets = Tweet.objects.all()
    context = {'tweets': tweets}
    if request.headers.get('X-Requested-With') == 'LikeButton':
        tweetID = request.headers.get('id')
        tweet = Tweet.objects.get(id=tweetID)
        json_context = {}

        try:
            like = tweet.tweetlike_set.filter(Q(author=request.user) & Q(tweet__id=tweetID))[0]
        except IndexError:
            like = None

        if like is None:
            like = TweetLike.objects.create(tweet=Tweet.objects.get(id=tweetID), author=request.user)
            like.save()
            json_context['action'] = 'liked'
        elif like is not None:
            like.delete()
            json_context['action'] = 'disliked'

        json_context['count'] = tweet.tweetlike_set.all().count()
        return JsonResponse(json_context)
    
    return render(request, 'pages/home_page.html', context)


def create_tweet_view(request):
    if request.method == 'POST':
        form = TweetCreationForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()

            return redirect('home')
        else:
            messages.error(request, 'Invalid data Check Out your inputs')
    else:
        form = TweetCreationForm()

    return render(request, 'pages/create_tweet_page.html', {'form': form})


def tweet_detail_view(request, pk):
    tweet = Tweet.objects.get(id=pk)
    replies = Reply.objects.filter(tweet=tweet)
    context = {
        'tweet': tweet,
        'replies': replies
    }
    return render(request, 'pages/tweet_detail_page.html', context)