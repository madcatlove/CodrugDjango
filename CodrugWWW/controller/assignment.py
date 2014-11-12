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


def assignment_list(request):

    assignmentList = Assignment.objects.all()

    rContext = RequestContext(request)
    ctx = Context({
        'aList' : assignmentList
    })
    rend = render(request, 'assignment.html', ctx, context_instance=rContext)
    return HttpResponse( rend )

'''
    과제 제출 컨트롤러
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