from django import forms
from .models import Reply


class TweetReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body', 'attachement']