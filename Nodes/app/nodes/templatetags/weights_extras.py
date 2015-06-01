from django import template

register = template.Library()


@register.filter(name='value_by_key')
def value_by_key(dict, key):
    try:
        return dict[key]
    except TypeError or KeyError:
        pass

