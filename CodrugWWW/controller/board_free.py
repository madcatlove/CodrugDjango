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
'''
def boardFree_write(request):

    ctx = Context({

    })

    tpl = get_template('boardFreeWrite.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)

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
