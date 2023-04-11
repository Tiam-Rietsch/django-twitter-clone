from django.apps import AppConfig


class TweetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweet'

    def ready(self):
        import os, subprocess
        from django.db.models.signals import pre_delete
        from tweet.models import Tweet
        from django.conf import settings
        
        def delete_atachement(sender, **kwargs):
            tweet = kwargs['linstance']
            # os.remove(os.path.join(settings.MEDIA_ROOT, tweet.attachement.name))

            # use this in production
            subprocess.run(['linode-cli', 'obj', 'del', 'twitter-clone-storage', tweet.attachement.name])


        pre_delete.connect(delete_atachement, sender=Tweet)
    
