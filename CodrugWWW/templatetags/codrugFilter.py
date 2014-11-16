# -*- coding: utf-8 -*-
from django import template
from ..models import  *

register = template.Library()

@register.filter(name = 'getSequence')
def getSequence(value, lastNum):
    return int( lastNum - value)


@register.filter(name = 'getLength')
def getLength(value):
    return len(value)


'''
    Image REF 정보를 던져주면 리스트 형식으로 리턴.
'''
@register.filter(name = 'getFileList')
def getFileList(image_ref):
    try:
        oFile = File.objects.filter( seq = image_ref)
        return oFile
    except:
        return []
