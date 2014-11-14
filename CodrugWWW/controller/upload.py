# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from ..models import *
from .. import utils
from .. import exceptions
import json


def downloadFile(request, fileSequence = -1):
    pass

def uploadFile(request):

    if request.method != 'POST':
        return HttpResponseForbidden()

    # 멤버 정보 확인.
    if not request.session.get('member_login'):
        return HttpResponseForbidden()

    # 파일 정보 확인.
    ## upFile 이라는 이름으로 올라옴.
    try:
        reqFile = request.FILES.getlist('upFile')
        if len(reqFile) == 0:
            raise exceptions.FileException(' 잘못된 요청입니다. ')

        try:
            lastImage = File.objects.latest('id')
            lastId = lastImage.id + 1
        except:
            lastId = 1

        # 파일 업로드
        rFile = utils.fileUploadSingle( reqFile[0] ) # 현재파일 , 변환파일, 파일 타입.

        # 데이터베이스에 기록.
        oFile = File( seq = lastId, inFILE = rFile[0], outFILE = rFile[1], typeFILE = rFile[2])
        oFile.save()

        # 파일 이름 리턴.
        json_message = utils.sMessage( data = rFile[1] )


    except exceptions.FileException, e:
        json_message = utils.sMessage( data = ' 잘못된 요청입니다. ', error = True)
    except Exception, e:
        json_message = utils.sMessage( data = ' 이미지 업로드를 실패하였습니다. ', error = True)



    return HttpResponse( json_message )



