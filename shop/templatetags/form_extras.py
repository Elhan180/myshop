from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def add_placeholder(field, text):
    return field.as_widget(attrs={
        "placeholder": text,
        "class": "form-control rounded-input"
    })
