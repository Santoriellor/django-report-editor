from django import template

register = template.Library()


@register.filter(name='capitalize_first')
def capitalize_first(value):
    if value:
        return value.capitalize()
    return value


@register.simple_tag
def total_count(initial=None, _count=[0]):  # noqa
    if initial is not None:
        # reset counter and make sure nothing is printed
        _count[0] = initial
        return ''
    # increment counter
    _count[0] += 1
    return _count[0]
