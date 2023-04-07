from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone

from .forms import TweetCreationForm
from .models import Tweet, TweetLike, Repost
from replies.models import Reply
from trends.models import Trend

def refresh_tweet_count(request):
    if request.headers['X-Requested-With'] == 'refreshTweetCount':
        old_count = int(request.GET.get('count'))
       
        if request.user.is_authenticated:
            new_count = Tweet.objects.exclude(author=request.user).count()
        else:
            new_count = Tweet.objects.all().count()

        json_context = {'has_new': old_count < new_count}
        return JsonResponse(json_context)


def check_tweet_existence(request):
    if request.headers['X-Requested-With'] == 'checkTweetExistence':
        try:
            tweet = Tweet.objects.get(id=int(request.GET.get('pk')))
        except Tweet.DoesNotExist:
            tweet = None

        if tweet == None:
            return JsonResponse({'exists': False})
        else:
            return JsonResponse({'exists': True})


def home_page_view(request):
    if request.user.is_authenticated:
        all_tweets = Tweet.objects.exclude(author=request.user)
    else:
        all_tweets = Tweet.objects.all()


    following_tweets = Tweet.objects.filter(author__profile__followers=request.user.profile) if request.user.is_authenticated else []
    context = {'all_tweets': all_tweets, 'following_tweets': following_tweets, 'topics': Trend.objects.all()}

    
    return render(request, 'pages/home_page.html', context)


def like_action(request):
    if request.headers.get('X-Requested-With') == 'LikeButton':
        tweetID = int(request.GET.get('pk'))
        tweet = Tweet.objects.get(id=tweetID)
        json_context = {}

        try:
            like = tweet.likes.filter(Q(author=request.user) & Q(tweet__id=tweetID))[0]
        except IndexError:
            like = None

        if like is None:
            like = TweetLike.objects.create(tweet=Tweet.objects.get(id=tweetID), author=request.user)
            like.save()
        elif like is not None:
            like.delete()
            json_context['disliked'] = True

        return JsonResponse(json_context)


def get_like_count(request):
    try:
        tweet_likes = Tweet.objects.get(id=int(request.GET.get('pk'))).likes.all()
        json_context = {
            'count': tweet_likes.count()
        }
        json_context['action'] = 'liked' if request.user in [like.author for like in tweet_likes] else 'disliked'
    except Tweet.DoesNotExist:
        json_context = {'error': True}

    return JsonResponse(json_context)


def get_repost_count(request):
    try:
        tweet = Tweet.objects.get(id=int(request.GET.get('pk')))
        all_repost = Repost.objects.filter(source_tweet=tweet)
        all_sources = Repost.objects.filter(repost_tweet=tweet)
        json_context = {
            'count': all_repost.count()
        }
        json_context['action'] = 'reposted' if request.user in [repost.author for repost in all_repost] else 'not reposted'
        json_context['is_a_repost'] = True if all_sources.count() > 0 else False
    except Tweet.DoesNotExist or Repost.DoesNotExist:
        json_context = {'error': True}

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
        tweet_to_repost = Tweet.objects.get(id=int(request.GET.get('pk')))

        try:
            primary_source = Repost.objects.get(Q(repost_tweet=tweet_to_repost) & Q(author=request.user)).source_tweet
            print(primary_source.author)
            print(Repost.objects.get(Q(source_tweet=primary_source) & Q(repost_tweet=tweet_to_repost)).author)
            is_retweeted = False
            if primary_source is not None:
                is_retweeted = True if request.user == Repost.objects.get(Q(source_tweet=primary_source) & Q(repost_tweet=tweet_to_repost)).author else False
        except Repost.DoesNotExist:
            primary_source = None
            is_retweeted = False


        try:
            current_repost = Repost.objects.get(Q(author=request.user) & Q(source_tweet=tweet_to_repost))
        except Repost.DoesNotExist:
            current_repost = None

        if current_repost is None and is_retweeted == False:                
            new_tweet = Tweet.objects.create(
                author=request.user,
                body=tweet_to_repost.body,
                attachement=tweet_to_repost.attachement,
            )

            new_tweet.save()
            repost = Repost.objects.create(
                author=request.user,
                source_tweet=tweet_to_repost,
                repost_tweet=new_tweet
            )
            repost.save()
        elif current_repost is not None:
            tweet = current_repost.repost_tweet
            tweet.delete()
            return JsonResponse({'deleted': True})
        elif is_retweeted == True:
            tweet_to_repost.delete()
            return JsonResponse({'deleted': True})

        
        return JsonResponse({'success': True})