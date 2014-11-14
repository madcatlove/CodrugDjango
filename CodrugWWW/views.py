# -*- coding: utf-8 -*-
import json
import os
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
import re
import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import *
from controller import member
from controller import board_free
from controller import timeline

'''
    Index page /
'''
def index(request):

    ctx = {}
    rContext = RequestContext(request)
    rend = render(request, 'index.html', ctx , context_instance = rContext)

    return HttpResponse( rend )

def testUpload(request):

    if request.method == 'POST':
        print request.FILES

        oFile = request.FILES.getlist('sUpload')
        print oFile
        for zFile in oFile:
            print zFile.name

    else :



        defaultPath = str(os.getcwd()).split('/')
        defaultPath.append('upload')
        uploadPath = '/'.join(defaultPath)
        if len(uploadPath) == 0:
            uploadPath = '/home/codrug/upload/'

        print uploadPath, len(uploadPath)

        rContext = RequestContext(request)
        ctx = {
            'uploadPath' : uploadPath,
        }
        rend = render(request, 'uploadTest.html', ctx, context_instance=rContext)

        return HttpResponse( rend )