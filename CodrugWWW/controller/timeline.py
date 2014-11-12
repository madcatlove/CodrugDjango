# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils

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
    for x in content:
        if x.image_ref > 0:
            oFile = File.objects.filter(id=x.image_ref)

            # 파일 분류작업
            for each in oFile:
                if re.search( r'\.(jpg|png|bmp)$', str(each.outFILE)):
                    oImg.append(each)
                else:
                    oEtc.append(each)

    ctx = {
        'content' : content,
        'imgList':oImg,
        'fileList':oEtc
    }

    rContext = RequestContext( request )
    htmlData = render(request, 'timeline.html.html', ctx, context_instance=rContext)

    return HttpResponse(htmlData)
