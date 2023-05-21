from django import template

register = template.Library()

@register.filter
def get_profile_picture(user):
    # use this in development for static files
    blank_profile_picture = '../static/img/blank-profile-picture.png'


    if user.profile.profile_picture:
        print(user)
        return user.profile.profile_picture.url 
    else:
        profile = user.profile
        profile.profile_picture = blank_profile_picture
        profile.save()
        get_profile_picture(user)


@register.filter
def get_cover_photo(user):
    # use this in development for static files
    blank_cover_photo = '../static/img/blank-cover-photo.png'

    if user.profile.cover_photo:
        return user.profile.cover_photo.url
    else:
        profile = user.profile
        profile.cover_photo = blank_cover_photo
        profile.save()
        get_cover_photo(user)


@register.filter
def is_following(user, connection):
    if user.profile in connection.followers.all():
        return True
    else:
        return False


