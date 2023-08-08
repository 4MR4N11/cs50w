from django import template
from django.template.defaultfilters import stringfilter
import markdown2 as md

"""
This is a custom template tag library for markdown.
"""
register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value)
