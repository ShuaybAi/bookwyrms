"""
Custom template tags and filters for the books app.
"""
from django import template
import json

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split a string by the given delimiter."""
    if value:
        return value.split(delimiter)
    return []

@register.filter
def safe_json(value):
    """Safely convert a dictionary to JSON string."""
    try:
        return json.dumps(value)
    except (TypeError, ValueError):
        return '{}'