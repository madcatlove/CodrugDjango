# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
import re
import math
from ..models import *

'''
    과제 리스트 컨트롤러
'''

def assignment_list(request):

    assignmentList = Assignment.objects.all()
    # 파일이 존재하면 이미지, 기타파일 분류작업.
    oImg = []
    oEtc = []
    for x in assignmentList:
        if x.image_ref > 0:
            oFile = File.objects.filter(id=x.image_ref)
            # 파일 분류작업
            for each in oFile:
                if re.search( r'\.(jpg|png|bmp)$', str(each.outFILE)):
                    oImg.append(each)
                else:
                    oEtc.append(each)
    rContext = RequestContext(request)
    ctx = {
        'aList' : assignmentList,
        'imgList' :oImg,
        'flieList':oEtc,
    }
    rend = render(request, 'assignment.html', ctx, context_instance=rContext)
    return HttpResponse( rend )

'''
    과제 생성 컨트롤러
'''
def assignment_write(request):

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    else:
        return HttpResponseForbidden()

'''
    과제 제출 상세보기
'''
def assignment_detail(request, articleId):
    pass


