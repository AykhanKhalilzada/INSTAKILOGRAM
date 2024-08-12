from django import template
from django.utils import timezone

from main.helpers.helpers import is_full

register = template.Library()

@register.filter(name='calculate_time_passed')
def calculate_time_passed(given_time, full=False) -> str:
    current_time = timezone.now()
    time_difference = current_time - given_time
    total_seconds = int(time_difference.total_seconds())
    
    limits = {0: 'second', 60: 'minute', 3600: 'hour', 86400: 'day', 604800: 'week'}
    sorted_limits = sorted(limits.keys())

    for i in range(len(sorted_limits)):
        limit = sorted_limits[i]
        if total_seconds < limit:
            previous_limit = sorted_limits[i-1]
            unit = limits[previous_limit]
            
            if previous_limit != 0:
                total_seconds = int(total_seconds / previous_limit)
            
            return f'{total_seconds}{is_full(full, unit, total_seconds)}'
    else:
        limit = sorted_limits[-1]
        unit = limits[limit]
        total_seconds = int(total_seconds / limit)
        return f'{total_seconds}{is_full(full, unit, total_seconds)}'

@register.filter(name='user_is_liked')
def user_is_liked(post, user) -> bool:
    return user.liked_posts.filter(pk__in=post.likes.values('pk')).exists()

@register.filter(name='user_is_saved')
def user_is_saved(post, user) -> bool:
    return user.saved_posts.filter(pk__in=post.saves.values('pk')).exists()

@register.filter(name='user_is_followed')
def user_is_followed(following, follower) -> bool:
    return follower.following.filter(pk__in=following.followers.values('pk')).exists()