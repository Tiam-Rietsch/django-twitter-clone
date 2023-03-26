from django import template

register = template.Library()

@register.filter
def get_profile_picture(user):
    print(user.username)
    if user.profile.profile_picture:
        return user.profile.profile_picture.url 
    else:
        profile = user.profile
        profile.profile_picture = '../static/img/blank-profile-picture.png'
        profile.save()
        get_profile_picture(user)


