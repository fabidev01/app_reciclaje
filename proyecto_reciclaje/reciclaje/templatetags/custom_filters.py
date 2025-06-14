from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of a substring in a string with another substring.
    Usage: {{ value|replace:"old:new" }}
    """
    if not value or not arg:
        return value
    try:
        s = str(value)
        old, new = arg.split(':')
        return s.replace(old, new)
    except ValueError:
        return s  # Retorna el valor original si el argumento no es válido