# core/templatetags/core_filters.py
from django import template

register = template.Library()

@register.filter
def underscore_to_space(value):
    """
    Replaces underscores with spaces in a string.
    Usage: {{ some_field_name|underscore_to_space }}
    """
    return value.replace('_', ' ')