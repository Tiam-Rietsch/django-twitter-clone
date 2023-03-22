from django.urls import path 
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),

    path('profile/<str:username>/', views.profile_page_view, name='profile-page'),
    path('follow-user/<int:profile_id>/', views.follow_user_view, name='follow-user')
]