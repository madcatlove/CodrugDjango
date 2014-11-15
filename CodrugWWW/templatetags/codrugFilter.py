
from django import template

register = template.Library()

@register.filter(name = 'getSequence')
def getSequence(value, lastNum):
    return int( lastNum - value)


@register.filter(name = 'getLength')
def getLength(value):
    return len(value)
