from django.apps import AppConfig
from django.contrib.auth import get_user_model

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import os, subprocess
        from django.conf import settings
        from django.db.models.signals import post_save, pre_delete
        from .models import Profile

        def delete_atachement(sender, **kwargs):
            # use this in development for static files
            # blank_profile_picture = '../static/img/blank-profile-picture.png'
            # blank_cover_photo = '../static/img/blank-cover-photo.png'

            # this is used for production
            blank_profile_picture = '../img/blank-profile-picture.png'
            blank_cover_photo = '../img/blank-cover-photo.png'

            profile = kwargs['instance']

            if profile.profile_picture != blank_profile_picture:
                # use this in development for static files
                # os.remove(os.path.join(settings.MEDIA_ROOT, profile.profile_picture.name))

                # use this in production
                subprocess.run(['linode-cli', 'obj', 'del', 'twitter-clone-storage', profile.profile_picture.name])


            if profile.cover_photo != blank_cover_photo:
                # use this in development for static files
                # os.remove(os.path.join(settings.MEDIA_ROOT, profile.cover_photo.name))

                # use this in production
                subprocess.run(['linode-cli', 'obj', 'del', 'twitter-clone-storage', profile.cover_photo.name])
   

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

                # use this in development for static files
                # blank_profile_picture = '../static/img/blank-profile-picture.png'
                # blank_cover_photo = '../static/img/blank-cover-photo.png'

                # this is used for production
                blank_profile_picture = '../img/blank-profile-picture.png'
                blank_cover_photo = '../img/blank-cover-photo.png'

                profile  = Profile.objects.create(user=user)
                profile.profile_picture = blank_profile_picture
                profile.cover_photo = blank_cover_photo
                profile.save()



        post_save.connect(set_username, sender=get_user_model())
        pre_delete.connect(delete_atachement, sender=Profile)

