# Generated by Django 4.1.7 on 2023-03-13 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_followers_alter_profile_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='followers',
        ),
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, to='users.profile'),
        ),
    ]
