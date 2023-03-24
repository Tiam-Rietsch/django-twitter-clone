from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone

from .forms import TweetCreationForm
from .models import Tweet, TweetLike, Repost
from replies.models import Reply

def home_page_view(request):
    all_tweets = Tweet.objects.all()

    following_tweets = Tweet.objects.filter(author__profile__followers=request.user.profile) if request.user.is_authenticated else []
    context = {'all_tweets': all_tweets, 'following_tweets': following_tweets}

    if request.headers.get('X-Requested-With') == 'LikeButton':
        tweetID = request.headers.get('id')
        tweet = Tweet.objects.get(id=tweetID)
        json_context = {}

        try:
            like = tweet.likes.filter(Q(author=request.user) & Q(tweet__id=tweetID))[0]
        except IndexError:
            like = None

        if like is None:
            like = TweetLike.objects.create(tweet=Tweet.objects.get(id=tweetID), author=request.user)
            like.save()
            json_context['action'] = 'liked'
        elif like is not None:
            like.delete()
            json_context['action'] = 'disliked'

        json_context['count'] = tweet.likes.all().count()
        return JsonResponse(json_context)
    
    return render(request, 'pages/home_page.html', context)


def get_like_count(request):
    tweet_likes = Tweet.objects.get(id=int(request.GET.get('pk'))).likes.all()
    json_context = {
        'count': tweet_likes.count()
    }
    json_context['action'] = 'liked' if request.user in [like.author for like in tweet_likes] else 'disliked'
    return JsonResponse(json_context)

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


def retweet_view(request):
    if request.headers['X-Requested-With'] == 'retweetButton':
        source = Tweet.objects.get(id=int(request.GET.get('pk')))
        new_tweet = Tweet.objects.create(
            author=request.user,
            body=source.body,
            attachement=source.attachement,
        )

        repost = Repost.objects.create(
            author=request.user,
            source=source
        )
        new_tweet.save()
        repost.save()
        return JsonResponse({'success': True})