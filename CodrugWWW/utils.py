# -*- coding: utf-8 -*-
from django.utils.html import strip_tags
import json

################
# Utility
################


'''
    주어진 문자 trim 후 모든 태그 제거
'''
def cleanStr( message ) :
    message = strip_tags( str(message).strip() )
    return message


'''
    json 을 위한 객체 ( error_message 가 있을경우 에러 메세지 리턴 )
'''
def sMessage( **kwargs ) :
    message = {}
    message['data'] = None
    message['error'] = True


    if 'error' in kwargs and kwargs.get('error') == True :
        message['error'] = True
    else :
        message['error'] = False

    if 'data' in kwargs :
        message['data'] = kwargs.get('data')
    else :
        message['data'] = None

    return json.dumps(message)