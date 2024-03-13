from django import template

register = template.Library()


@register.filter(name='capitalize_first')
def capitalize_first(value):
    if value:
        return value.capitalize()
    return value
