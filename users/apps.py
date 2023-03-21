from django.apps import AppConfig
from django.contrib.auth import get_user_model

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.db.models.signals import post_save
        from .models import Profile

        def set_username(sender, **kwargs):
            if kwargs['created']:
                user = kwargs['instance']
                first_names = user.first_name.split()
                last_names = user.last_name.split()

                if len(first_names) > 1:
                    user.username = first_names[0] + first_names[1]
                else:
                    user.username = first_names[0] + last_names[0]

                user.username = user.username.lower()
                user.email = user.email.lower()
                user.save()

                Profile.objects.create(user=user).save()

        post_save.connect(set_username, sender=get_user_model())