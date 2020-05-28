from django import template

from ..models import VideoType, FromType, IdentityType

register = template.Library()


def get_video_type_label(value):
    return VideoType(value).label


def get_from_label(value):
    return FromType(value).label


def get_star_label(value):
    return IdentityType(value).label


register.filter('get_video_type_label', get_video_type_label)
register.filter('get_from_label', get_from_label)
register.filter('get_star_label', get_star_label)
