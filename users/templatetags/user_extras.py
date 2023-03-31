from django import template

register = template.Library()

@register.filter
def get_profile_picture(user):
    if user.profile.profile_picture:
        return user.profile.profile_picture.url 
    else:
        profile = user.profile
        profile.profile_picture = '../static/img/blank-profile-picture.png'
        profile.save()
        get_profile_picture(user)


@register.filter
def get_cover_photo(user):
    if user.profile.cover_photo:
        return user.profile.cover_photo.url
    else:
        profile = user.profile
        profile.cover_photo = '../static/img/blank-cover-photo.png'
        profile.save()
        get_cover_photo(user)


