from django import template

register = template.Library()

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
            word_dict['type'] = 'has-tag'
        else:
            word_dict['type'] ='text'

        word_dict['word'] = word

        final_list.append(word_dict)

    return final_list
   

@register.filter    
def get_value(dictionary, key):
    return dictionary[key]