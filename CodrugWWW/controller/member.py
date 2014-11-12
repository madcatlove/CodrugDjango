# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render

from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
from ..models import *

'''
    Member join page /member/join
'''
def member_join(request):

    # -- GET -- >> View rendering
    if request.method == 'GET' :
        ctx = Context({

        })
        rContext = RequestContext( request )
        htmlData = render(request, 'member_join.html', ctx, context_instance=rContext)
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

    json_message = {}
    # POST DATA
    try:
        user_email = utils.cleanStr( request.POST.get('email') )
        user_password = utils.cleanStr( request.POST.get('password') )

        oMember = Member.objects.get(email = user_email)

        if oMember == None :
            json_message = utils.sMessage( data = '로그인 실패', error = True)
        elif oMember.email != user_email or oMember.password != user_password :
            json_message = utils.sMessage( data = '로그인 실패', error = True)
        else :
            # 로그인 성공
            request.session['member_login'] = {
                'seq' : oMember.id,
                'email' : oMember.email
            }
            json_message = utils.sMessage( data = oMember.id)


    except (Member.DoesNotExist, KeyError) as e:
        json_message = utils.sMessage( data = '로그인 실패', error = True)


    return HttpResponse( json.dumps(json_message) )

'''
    Member logout /member/logout
'''
def member_logout(request):
    del request.session['member_login']
    json_message = utils.sMessage(data = '정상적으로 로그아웃 되었습니다.')
    return HttpResponse( json.dumps(json_message) )




'''
    Member list page /member/list
'''
def member_list(request):

    mList = Member.objects.all()
    print mList

    ctx = Context({
        'mlist' : mList
    })

    rContext = RequestContext( request )
    htmlData = render(request, 'members.html', ctx, context_instance=rContext)
    return HttpResponse( htmlData )

