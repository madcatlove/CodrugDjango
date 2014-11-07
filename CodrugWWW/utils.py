# -*- coding: utf-8 -*-
import hashlib
from django.utils.html import strip_tags
import json
import os

################
# Utility
################
import time


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


'''
    파일 업로드 함수.
    request.FILES 요구 , 파일을 담고있는 key 값 요구.

    request.FILES['file_form_name']

    리턴 (원본파일이름, 변환된파일이름, 파일타입)
'''
def fileUpload( oFile, keyName ):
    defaultPath = str(os.getcwd()).split('/')
    defaultPath.append('upload')

    uploadPath = '/'.join(defaultPath)

    # calculate file upload
    file = oFile[keyName]
    fileName =  unicode( file.name )
    extension = fileName.split('.')
    extension = extension[ len(extension) -1 ]
    transfilename = '%s.%s' % (hashlib.md5(fileName).hexdigest() + str(int(time.time()) ), extension )

    # upload file
    try:
        with open( '%s/%s' % (uploadPath, transfilename) , 'wb') as fp :
            for chunk in file.chunks():
                fp.write(chunk)

        return ( fileName, transfilename, file.content_type )
    except:
        return (None, None, None)


def getBoardExtraMessage(**kwargs) :
    # default message
    message = {
        'isConfirmed' : False
    }

    for sKey in kwargs:
        message[sKey] = kwargs[sKey]

    return json.dumps(message)
