# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
import utils

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

    # -- GET -- >> View rendering
    if request.method == 'GET' :
        tpl = get_template('member_join.html')
        htmlData = tpl.render( Context() )
        return HttpResponse( htmlData )

    # -- POST -- >> Post form
    elif request.method == 'POST' :

        # GET DATA
        user_password = utils.cleanStr( request.POST.get('password'))
        user_email = utils.cleanStr( request.POST.get('email') )
        user_name = utils.cleanStr( request.POST.get('name') )

        json_message = {}

        # Validation
        if len(user_password) == 0 or len(user_email) == 0 or len(user_name) == 0 :
            json_message = utils.sMessage( data = '잘못된 정보입니다', error = True)
        else :
            try:
                oMember = Member(email = user_email, password = user_password, name = user_name, extra = '')
                oMember.save()
                json_message = utils.sMessage( data = 'Success')
            except IntegrityError:
                json_message = utils.sMessage( data = '회원생성중 에러', error = True)



        return HttpResponse(json_message)

    # -- Others >> Error (403)
    else :
        return HttpResponseForbidden()



'''
    Member Login page /member/login
'''
def member_login(request):
    pass


'''
    Member list page /member/list
'''
def member_list(request):

    mList = Member.objects.all()
    print mList

    ctx = Context({
        'mlist' : mList
    })

    tpl = get_template('members.html')
    htmlData = tpl.render( ctx )

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
    })

    tpl = get_template('boardFreeList.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)