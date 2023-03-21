from django import forms
from .models import Tweet


class TweetCreationForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['body', 'attachement']
