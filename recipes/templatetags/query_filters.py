from django import template

register = template.Library()


@register.filter
def get_item(key, dictionary=None):
    if dictionary is None or not hasattr(dictionary, 'get'):
        dictionary = {'info': 'Info', 'success': 'Success', 'warning': 'Warning', 'danger': 'Error'}

    return dictionary.get(key)
