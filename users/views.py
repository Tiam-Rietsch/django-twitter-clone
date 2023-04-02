import json, os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse

from tweet.models import Tweet, TweetLike
from replies.models import Reply
from .forms import RegisterForm, EditProfileForm
from .models import User, Profile

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
        'replied_tweets': replied_tweets
    }
    return render(request, 'pages/profile_page.html', context)


def edit_profile_view(request, profile_id):
    if request.method == 'POST':
        profile = Profile.objects.get(id=profile_id)
        cover_photo = request.FILES.get('cover-image')
        profile_picture = request.FILES.get('profile-picture')
        username = request.POST.get('username')
        bio = request.POST.get('bio')

        profile.cover_photo = cover_photo
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


def follow_user_view(request, profile_id):
    to_follow = User.objects.get(id=profile_id)

    if request.user.profile in to_follow.profile.followers.all():
        to_follow.profile.followers.remove(request.user.profile)
        return JsonResponse({'followed': False})
    else:
        to_follow.profile.followers.add(request.user.profile)
        return JsonResponse({'followed': True})


