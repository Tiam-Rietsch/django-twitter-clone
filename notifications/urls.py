from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/notifications/', views.notification_page_view, name='notifications'),
    path('get-unviewed-notifications', views.get_unviewed_notifications, name='get-unviewed-notifications'),
]