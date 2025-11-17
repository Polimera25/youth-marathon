from django import template

register = template.Library()

@register.filter(name='as_widget')
def as_widget(value, arg):
    """
    Adds CSS classes to form widgets.
    Usage example in template:
    {{ form.name|as_widget:"class=border p-2 rounded" }}
    """
    attrs = {}
    kv = arg.split('=')
    if len(kv) == 2:
        attrs[kv[0]] = kv[1]
    return value.as_widget(attrs=attrs)
