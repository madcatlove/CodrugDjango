# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context
import re
from ..models import *


def timeline(request,):

    content = {}
    content = Board.objects.all()
    if content.image_ref > 0:
        oFile = File.objects.filter(id=content.image_ref)
        oImg=[]
        oEtc=[]
        for each in oFile:
            if re.search( r'\.(jpg|png|bmp)$', str(each.outFILE)):
                oImg.append(each)
            else:
                oEtc.append(each)
    else:
        oFile = []
        oImg=[]
        oEtc=[]

    ctx = Context({
        'content' : content,
        'imgList':oImg,
        'fileList':oEtc
    })

    tpl = get_template('timeline.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)
