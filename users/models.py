from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profiles/profile_pictures/')
    cover_photo = models.ImageField(blank=True, null=True,  upload_to='profiles/cover_photos/')
    date_joined = models.DateField(auto_now_add=True)
    followers = models.ManyToManyField('Profile', blank=True, null=True)

    def __str__(self):
        return self.user.email
