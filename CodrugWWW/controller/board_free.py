# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context
from ..models import *


'''
    Freeboard write
    GET method 로 접근시 글쓰기 폼을 보여주며
    POST method 로 접근시 글쓰기 작업을 진행한다.
'''
def boardFree_write(request):

    if request.method == 'GET' :
        ctx = Context({

        })

        tpl = get_template('boardFreeWrite.html')
        htmlData = tpl.render( ctx )

        return HttpResponse(htmlData)
    elif request.method == 'POST':
        print request.POST
        print request.FILES
        print request.session


        board_title = utils.cleanStr( request.POST.get('board_title') )
        board_title = request.POST.get('board_content').strip()



    else:
        return HttpResponseForbidden();

'''
    Freeboard list
'''
def boardFree_list(request, page = 1):
    if len(str(page)) == 0: page = 1

    ctx = Context({
        'page' : page,
        'boardName' : 'free',
    })

    tpl = get_template('boardFreeList.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)
