# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template
from django.template import Context
from models import *

'''
    Index page /
'''
def index(request):
    tpl = get_template('index.html')
    htmlData = tpl.render( Context() )

    #htmlData = "Hello world."


    return HttpResponse(htmlData)

'''
    Member join page /member/join
'''
def member_join(request):

    print request.method

    # -- GET -- >> View rendering
    if request.method == 'GET' :
        tpl = get_template('member_join.html')
        htmlData = tpl.render( Context() )
        return HttpResponse( htmlData )

    # -- POST -- >> Post form
    else :
        print 'hello'
        return HttpResponse('Hello')

    # -- Others >> Error (403)
    #else :
    #    return HttpResponseForbidden()



'''
    Member Login page /member/login
'''
def member_login(request):
    pass

def member_list(request):
    tpl = get_template('members.html')
    htmlData = tpl.render( Context() )

    return HttpResponse( htmlData )



def qna_list(request, page = '1'):
    print page
    try:
        page = int(page)
    except ValueError:
        raise Http404()

    sParam = {
        'page' : page
    }

    tpl = get_template('qna.html')
    htmlData = tpl.render( Context(sParam) )

    return HttpResponse(htmlData)


def timeline(request,):
    ctx = Context({
    })
    content = {}
    content = Board.objects.all()
    ctx = Context({
        'content' : content
    })

    tpl = get_template('timeline.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)