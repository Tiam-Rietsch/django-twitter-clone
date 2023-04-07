from django.apps import AppConfig


class TrendsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trends'


    def ready(self):
        from django.db.models.signals import pre_save
        from .models import Trend
        from tweet.models import Tweet

        def update_trending_topics(sender, **kwargs):
                tweet = kwargs['instance']
                word_list = set(word for word in tweet.body.split() if '#' in word)

                try:
                    saved_tweet = Tweet.objects.get(id=tweet.id)
                    word_list = word_list.difference(set(word for word in saved_tweet.body.split() if '#' in word))
                except Tweet.DoesNotExist:
                     pass
                
                for word in word_list:
                    try:
                        trend = Trend.objects.get(name=word)
                        trend.tweet_count += 1
                        trend.save()
                    except Trend.DoesNotExist:
                        Trend.objects.create(name=word, tweet_count=1).save()


                trends_count = Trend.objects.all().count()
                if trends_count >= 100:
                    for trend in Trend.objects.all()[26:trends_count - 1]:
                        trend.delete()

        pre_save.connect(update_trending_topics, sender=Tweet)