from django import template

register = template.Library()

@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) + 1] # access the next element
    except:
        return '' # return empty string in case of exception

@register.filter
def previous(some_list, current_index):
    """
    Returns the previous element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        if int(current_index) - 1 >= 0:
            return some_list[int(current_index) - 1]
        else:
            return ''
    except:
        return '' # return empty string in case of exception

@register.simple_tag
def define():
  return False
