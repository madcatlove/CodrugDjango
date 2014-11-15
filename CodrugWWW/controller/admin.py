
# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden, QueryDict
from django.shortcuts import render

from .. import utils, exceptions

# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
import re
from ..models import *


def adminIndex(request):
    ctx = {

    }
    rContext = RequestContext(request)
    htmlData = render(request, 'include/admin_layout.html', ctx, context_instance=rContext)

    return HttpResponse(htmlData)

'''
    관리자 -> 회원관리 기능
'''
def adminMember(request):

    oMember = Member.objects.all().order_by('-id')

    print oMember[0].id

    # HTML Rendering
    ctx = {
        'member' : oMember,
    }
    rContext = RequestContext(request)
    htmlData = render(request, 'admin_member.html', ctx, context_instance = rContext)
    return HttpResponse(htmlData)


'''
    관리자 -> 회원관리 기능(처리)
    request.METHOD 에 따라 다른 처리
    (PUT -> UPDATE , DELETE-> DELETE RECORD )
'''
def adminMemberProc(request, memberId):
    print memberId,

    print request.method
    try:
        print QueryDict( request.body )

    except Exception, e:
        print e


'''
    관리자 -> 과제 제출(쓰기)
'''
def adminAssignmentWrite(request):

    if request.method == 'GET':
        ctx = {

        }
        rContext = RequestContext(request)
        htmlData = render(request, 'admin_assignmentWrite.html', ctx, context_instance=rContext)

        return HttpResponse(htmlData)
    else:
        pass


'''
    관리자 -> 과제 리스트
'''
def adminAssignmentList(request):
    pass

'''
    관리자 유무 판단
    ( 내부적으로 사용 )
    // true , false 리턴.
'''
def _privIsAdmin( requestData ):
    pass