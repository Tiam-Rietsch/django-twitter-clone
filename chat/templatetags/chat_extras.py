from django import template
from django.db.models import Q

register = template.Library()


@register.filter
def get_room_display_profile(room, request_user):
    profile = [profile for profile in room.participants.all() if profile.user.username != request_user.username][0]
    return profile
