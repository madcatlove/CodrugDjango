
from django import template

register = template.Library()

@register.filter(name = 'getSequence')
def getSequence(value, lastNum):
    return int( lastNum - value)

