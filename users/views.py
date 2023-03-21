import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm
from .models import User

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
