from django.shortcuts import render, redirect
from tweet.models import Tweet

from .forms import TweetReplyForm

def tweet_reply_view(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)

    if request.method == 'POST':
        form = TweetReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.tweet = tweet
            reply.save()

            return redirect('tweet-detail', pk=tweet_id)
    else:
        form = TweetReplyForm()


    return render(request, 'pages/tweet_reply_page.html', {'form': form, 'tweet_id': tweet_id})