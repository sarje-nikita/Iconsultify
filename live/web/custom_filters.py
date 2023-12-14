from django import template

register = template.Library()

@register.filter
def replace(value, find, replace):
    return value.replace(find, replace)