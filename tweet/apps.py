from django.apps import AppConfig


class TweetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweet'

    def ready(self):
        import os
        from django.db.models.signals import pre_delete
        from tweet.models import Tweet
        from django.conf import settings
        
        def delete_atachement(sender, **kwargs):
            tweet = kwargs['instance']
            os.remove(os.path.join(settings.MEDIA_ROOT, tweet.attachement.name))


        pre_delete.connect(delete_atachement, sender=Tweet)
    
