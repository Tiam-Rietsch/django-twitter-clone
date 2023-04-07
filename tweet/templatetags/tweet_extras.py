from django import template

register = template.Library()


@register.filter
def has_liked(user, tweet_id):
    from tweet.models import Tweet

    tweet = Tweet.objects.get(id=tweet_id)
    tweet_likes_users = [like.author for  like in tweet.likes.all()]
    if user in tweet_likes_users:
        return True
    else:
        return False


@register.filter
def format_tweet_text(text):
    word_list = text.split()
    final_list = []

    for word in word_list:
        word_dict = {}
        if word.startswith('@'):
            word_dict['word'] = word
            word_dict['type'] = 'username'
        elif word.startswith('#'):
            word_dict['type'] = 'hashtag'
        else:
            word_dict['type'] ='text'

        word_dict['word'] = word

        final_list.append(word_dict)

    return final_list
   
@register.filter 
def remove_decorator(word_dictionary):
    return ''.join(character for character in word_dictionary['word'] if character.isalnum())

@register.filter    
def get_value(dictionary, key):
    return dictionary[key]

@register.filter
def get_specific_reply(tweet, user):
    return tweet.reply_set.filter(author=user)

@register.filter
def get_like_count(tweet_id):
    from tweet.models import Tweet
    
    tweet = Tweet.objects.get(id=tweet_id)
    return tweet.likes.all().count()
    

@register.filter
def get_latest_retweet(user):
    from tweet.models import Tweet, Repost
    from users.models import User

    author = User.objects.get(id=user.id)
    latest_tweet = Tweet.objects.all()[0]

    if author in [repost.author for repost in Repost.objects.all()]:
        return latest_tweet
    else:
        return None
    

@register.filter
def get_bio_summary(bio):
    if bio is not None:
        return bio[:100] + "..."
    else:
        return "..."