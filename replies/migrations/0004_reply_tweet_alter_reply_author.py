# Generated by Django 4.1.7 on 2023-03-20 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0002_alter_tweet_options_tweet_date_created'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('replies', '0003_alter_reply_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='tweet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tweet.tweet'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]