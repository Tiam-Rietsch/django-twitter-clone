import os, subprocess
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse

from tweet.models import TweetLike
from replies.models import Reply
from .forms import RegisterForm
from .models import User, Profile
from trends.models import Trend
from notifications.models import Notification
def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')   
    else:
        form = RegisterForm()

    
    return render(request, 'pages/login_register_page.html', {'form': form, 'register': True})


def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Username not found")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        elif user is None:
            messages.error(request, "somehting went wrong")

    return render(request, 'pages/login_register_page.html')


def profile_page_view(request, username):
    profile = Profile.objects.get(user__username=username)
    followers = profile.followers.all()
    following = Profile.objects.filter(followers__user__username=username)
    profile_tweets = profile.user.tweet_set.all()
    liked_tweets = [like.tweet for like in TweetLike.objects.filter(author__username=username)]
    replied_tweets = set(reply.tweet for reply in Reply.objects.filter(author__username=username))
    context = {
        'profile': profile,
        'followers': followers,
        'following': following,
        'profile_tweets': profile_tweets,
        'liked_tweets': liked_tweets,
        'replied_tweets': replied_tweets,
        'topics': Trend.objects.all(),
    }
    return render(request, 'pages/profile_page.html', context)


def edit_profile_view(request, profile_id):
    if request.method == 'POST':
        profile = Profile.objects.get(id=profile_id)
        cover_photo = request.FILES.get('cover-image')
        profile_picture = request.FILES.get('profile-picture')
        username = request.POST.get('username')
        bio = request.POST.get('bio')

        # use this in development for static files
        # blank_profile_picture = 'static/img/blank-profile-picture.png'
        # blank_cover_photo = 'static/img/blank-cover-photo.png'

        # this is used for production
        blank_profile_picture = '/img/blank-profile-picture.png'
        blank_cover_photo = '/img/blank-cover-photo.png'

        if cover_photo:
            if profile.cover_photo.url != blank_cover_photo: 
                subprocess.run(['linode-cli', 'obj', 'del', 'twitter-clone-storage', profile.cover_photo.name])

                # in development when MEDIA_ROOT is set
                # os.remove(os.path.join(settings.MEDIA_ROOT, profile.cover_photo.name))

            profile.cover_photo = cover_photo

        if profile_picture:
            if profile.profile_picture.url != blank_profile_picture:
                subprocess.run(['linode-cli', 'obj', 'del', 'twitter-clone-storage', profile.profile_picture.name])

                # in development when MEDIA_ROOT is set
                # os.remove(os.path.join(settings.MEDIA_ROOT, profile.profile_picture.name))


    
            profile.profile_picture = profile_picture

        profile.bio = bio
        profile.save()
        profile.user.username = username
        profile.user.save()

        return redirect('profile-page', username=username)
        
    context = {
        'profile' :Profile.objects.get(id=profile_id)
    }
    return render(request, 'pages/edit_profile_page.html', context)


def follow_user_view(request, user_id):
    to_follow = User.objects.get(id=user_id)

    if request.user.profile in to_follow.profile.followers.all():
        to_follow.profile.followers.remove(request.user.profile)
        try:
            notice = Notification.objects.get(
                receiver=to_follow.profile,
                sender=request.user.profile,
                title='New Follower',
                body=f'user @{request.user.username} started following you'
            )
            notice.delete()
        except Notification.DoesNotExist:
            pass

        return JsonResponse({'followed': False})
    else:
        to_follow.profile.followers.add(request.user.profile)
        notice = Notification.objects.create(
            receiver=to_follow.profile,
            sender=request.user.profile,
            title='New Follower',
            body=f'user @{request.user.username} started following you'
        )
        notice.save()
        return JsonResponse({'followed': True})


def follow_connection_view(request):
    to_follow = User.objects.get(id=int(request.GET.get('user_id')))

    if request.user.profile in to_follow.profile.followers.all():
        to_follow.profile.followers.remove(request.user.profile)
        try:
            notice = Notification.objects.filter(
                receiver=to_follow.profile,
                sender=request.user.profile,
                title='New Follower',
                body=f'user @{request.user.username} started following you'
            )[0]
            notice.delete()
        except Notification.DoesNotExist:
            pass

        return JsonResponse({'followed': False})
    else:
        to_follow.profile.followers.add(request.user.profile)
        notice = Notification.objects.create(
            receiver=to_follow.profile,
            sender=request.user.profile,
            title='New Follower',
            body=f'user @{request.user.username} started following you'
        )
        notice.save()
        return JsonResponse({'followed': True})



def following_list_view(request, user_id):
    user = User.objects.get(id=user_id)
    following = Profile.objects.filter(followers__user=user)
    return render(request, 'pages/followers_following_page.html', {'connections': following, 'topics': Trend.objects.all()})


def followers_list_view(request, user_id):
    user = User.objects.get(id=user_id)
    followers = user.profile.followers.all()
    return render(request, 'pages/followers_following_page.html', {'connections': followers, 'topics': Trend.objects.all()})

