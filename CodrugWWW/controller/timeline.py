# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils
import random
# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
import re
from ..models import *


def timeline(request,):
    content = {}
    content = Board.objects.all()
    # 파일이 존재하면 이미지, 기타파일 분류작업.
    oImg = []
    oEtc = []
    # 게시물에 이미지 정보 주입.
    for idx in range(0, len(content)):
        if content[idx].image_ref > 0 :
            fileList = File.objects.filter( seq = content[idx].image_ref )
            oRandomFile = fileList[random.randint(0,len(fileList)-1)]
            # content[idx].fileList = fileList
            content[idx].oFile = oRandomFile


    ctx = {
        'content' : content,
    }

    rContext = RequestContext( request )
    htmlData = render(request, 'timeline.html', ctx, context_instance=rContext)

    return HttpResponse(htmlData)
