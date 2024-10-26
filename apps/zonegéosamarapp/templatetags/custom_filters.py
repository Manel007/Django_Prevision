from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """Add a class to a form field."""
    return field.as_widget(attrs={'class': css_class})


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})