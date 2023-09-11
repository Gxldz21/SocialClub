from django import template
from multiclub.models import *
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})

@register.filter
def get_user_avatar(user_avatar, user_id):
    return user_avatar.filter(user_id=user_id).first()