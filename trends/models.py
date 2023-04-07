from django.db import models

# Create your models here.
class Trend(models.Model):
    name = models.CharField(max_length=200, unique=True)
    tweet_count = models.IntegerField()

    class Meta:
        ordering = ['-tweet_count']

    def __str__(self):
        return self.name
    