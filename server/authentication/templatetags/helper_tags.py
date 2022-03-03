from django import template

register = template.Library()

@register.filter(name='modulo')
def modulo(value,attr):
  value = int(value)
  attr = int(attr)
  return value%attr

@register.filter(name='get_value')
def get_value(dictionary, key):
  return dictionary.get(key)
