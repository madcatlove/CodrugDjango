# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render

from .. import utils, exceptions

# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
import re
from ..models import *

'''
    Member join page /member/join
'''
def member_join(request):

    # -- GET -- >> View rendering
    if request.method == 'GET' :
        ctx = {

        }
        rContext = RequestContext( request )
        htmlData = render(request, 'member_join.html', ctx, context_instance=rContext)
        return HttpResponse( htmlData )

    # -- POST -- >> Post form
    elif request.method == 'POST' :

        try:
            # GET DATA
            user_password = utils.cleanStr( request.POST.get('password'))
            user_email = utils.cleanStr( request.POST.get('email') )
            user_name = utils.cleanStr( request.POST.get('name') )

            # 유저 이메일 / 비밀번호 길이 체크.
            if len(user_email) == 0 or len(user_password) == 0 or len(user_name) == 0:
                raise exceptions.MemberException(' 필수 항목이 누락되었습니다. ')

            # 이메일 유효성 검사 시작.
            sRegex = re.compile( r'^[\w\.\-\_]+@[\w\_\-]+\.[\w\.]+[^\W]$' )
            if bool( sRegex.match( user_email ) ) != True:
                raise exceptions.MemberException(' 이메일 주소가 올바르지 않습니다. ')

            # Commit
            oMember = Member(email = user_email, password = user_password, name = user_name, extra = '')
            oMember.save()
            json_message = utils.sMessage( data = 'Success')



        except exceptions.MemberException, e:
            json_message = utils.sMessage( data = e.message, error = True)

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

    if request.method != 'POST':
        return HttpResponseForbidden()

    json_message = {}
    # POST DATA
    try:

        user_email = utils.cleanStr( request.POST.get('email') )
        user_password = utils.cleanStr( request.POST.get('password') )

        # 유저 이메일 / 비밀번호 길이 체크.
        if len(user_email) == 0 or len(user_password) == 0:
            raise exceptions.MemberException(' 아이디나 비밀번호가 누락되었습니다. ')

        # 이메일 유효성 검사 시작.
        sRegex = re.compile( r'^[\w\.\-\_]+@[\w\_\-]+\.[\w\.]+[^\W]$' )
        if bool( sRegex.match( user_email ) ) != True:
            raise exceptions.MemberException(' 이메일 주소가 올바르지 않습니다. ')

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

    except exceptions.MemberException, e:
        json_message = utils.sMessage( data = e.message, error = True)


    except (Member.DoesNotExist, KeyError, TypeError) as e:
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

    ctx = {
        'mlist' : mList
    }

    rContext = RequestContext( request )
    htmlData = render(request, 'members.html', ctx, context_instance=rContext)
    return HttpResponse( htmlData )


'''
    Member Modify form
'''
def member_modify(request):

    # Globally check member logged
    memberSession = request.session.get('member_login')
    if not memberSession or memberSession.seq < 0:
        return HttpResponse( utils.scriptError(' 회원 로그인이 필요한 페이지입니다. ', '/') )

    # Get Member info
    try:
        oMember = Member.objects.get( id = memberSession.seq )
    except Member.DoesNotExist, e:
        del request.session['member_login']
        return HttpResponse( utils.scriptError(' 회원 정보를 가져올 수 없습니다. ', '/') )



    if request.method == 'GET':
        # Rendering View page
        ctx = {
            'member' : oMember,
        }
        rContext = RequestContext(request)
        htmlData = render( request, 'memberModify.html', ctx, context_instance = rContext)
        return HttpResponse( htmlData )

    elif request.method == 'POST':
        pass

    else:
        return HttpResponseForbidden()