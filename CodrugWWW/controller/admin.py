
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

    if not _privIsAdmin(request):
        return HttpResponse( utils.scriptError(' 관리자 로그인이 필요한 페이지입니다. ') )

    ctx = {

    }
    rContext = RequestContext(request)
    htmlData = render(request, 'include/admin_layout.html', ctx, context_instance=rContext)

    return HttpResponse(htmlData)

'''
    관리자 -> 회원관리 기능
'''
def adminMember(request):

    if not _privIsAdmin(request):
        return HttpResponse( utils.scriptError(' 관리자 로그인이 필요한 페이지입니다. ') )

    oMember = Member.objects.all().order_by('-id')

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

    try:
        # Admin Auth
        if not _privIsAdmin(request):
            raise exceptions.MemberException(' 관리자 권한이 필요한 페이지 입니다. ')

        # PUT ( update member )
        if request.method == 'PUT':
            rData = QueryDict( request.body ) # BODY 부분 딕셔너리 형태로 재 가공.
            memberSeq = int( rData.get('seq') )
            memberPassword = rData.get('password')
            memberName = utils.cleanStr( rData.get('name') )
            memberLevel = int( rData.get('level') )

            oMember = Member.objects.get( id = memberSeq )
            oMember.name = memberName
            if len(memberPassword) != 0:
                oMember.password = utils.cryptPassword( memberPassword )
            oMember.level = memberLevel

            oMember.save()

            return HttpResponse( utils.sMessage( data = ' 정상적으로 업데이트 하였습니다. ') )

        # DELETE ( member delete )
        elif request.method == 'DELETE':
            memberId = int( memberId )
            oMember = Member.objects.get( id = memberId )
            oMember.delete()

            return HttpResponse( utils.sMessage( data = ' 정상적으로 삭제하였습니다. '))

        else:
            raise Exception

    except Exception, e:
        return HttpResponse( utils.sMessage( data = e.message , error = True) )



'''
    관리자 -> 과제 제출(쓰기)
'''
def adminAssignmentWrite(request):

    if not _privIsAdmin(request):
        return HttpResponse( utils.scriptError(' 관리자 로그인이 필요한 페이지입니다. ') )

    if request.method == 'GET':
        ctx = {

        }
        rContext = RequestContext(request)
        htmlData = render(request, 'admin_assignmentWrite.html', ctx, context_instance=rContext)

        return HttpResponse(htmlData)
    else:
        try:
            workTitle =  utils.cleanStr( request.POST.get('workTitle') )
            workContent = request.POST.get('workContent')
            workDeadline = utils.cleanStr( request.POST.get('workDeadline') )
            workFile = request.FILES.getlist('workFile')


            if len(workTitle) == 0 or len( utils.cleanStr(workContent) ) == 0 or len(workDeadline) == 0:
                raise exceptions.AssignmentException(' 필요한 정보가 모두 오지 않았습니다. ')

            ##---------------------------------------
            ## FILE UPLOAD ( Processing Multiple uploads )
            ##---------------------------------------
            # 파일 리스트가 0 개가 아니라면 업로드 처리.
            if len(workFile) != 0:
                # 최근 이미지 번호를 가져와 +1 ( 없으면 1로 설정 )
                try:
                    lastImage = File.objects.latest('id')
                    lastId = lastImage.id + 1
                except :
                    lastId = 1

                # 파일 업로드 처리.
                for fileData in workFile:
                    rFile = utils.fileUploadSingle( fileData ) # 리턴값 : (원본파일이름, 변환파일이름, 파일타입)
                    if rFile[0] is not None:
                        oImage = File( seq = lastId, inFILE = rFile[0], outFILE = rFile[1], typeFILE = rFile[2])
                        oImage.save()
            else:
                lastId = -1


            # Assigment 등록
            oAssignment = Assignment( title = workTitle, content = workContent, deadline = workDeadline, image_ref = lastId)
            oAssignment.save()

            #
            return HttpResponse( utils.scriptError(' 정상적으로 등록하였습니다. ') )


        except exceptions.AssignmentException, e:
            return HttpResponse( utils.scriptError( e.message ) )
        except Exception, e:
            return HttpResponse( utils.scriptError(' Fatal error occured ') )

'''
    관리자 -> 과제 리스트
'''
def adminAssignmentList(request):

    if not _privIsAdmin(request):
        return HttpResponse( utils.scriptError(' 관리자 로그인이 필요한 페이지입니다. ') )

    # 과제리스트 가져옴.
    oAssignment = Assignment.objects.all().order_by('-id')

    # 과제 리스트에 제출 리스트 등록.
    for idx in range(0, len(oAssignment)):
        oSubmit = Submit.objects.filter( assignmentID = oAssignment[idx] )
        oAssignment[idx].submitlist = oSubmit
        oAssignment[idx].countsubmitlist = len(oSubmit)




    # HTML Rendering
    ctx = {
        'assignmentlist' : oAssignment,
    }
    rContext = RequestContext( request )
    htmlData = render( request, 'admin_assignmentList.html', ctx, context_instance = rContext)
    return HttpResponse( htmlData )

'''
    관리자 유무 판단
    ( 내부적으로 사용 )
    // true , false 리턴.
'''
def _privIsAdmin( requestData ):
    memberSession = requestData.session['member_login']
    if not memberSession:
        return False

    try:
        oMember = Member.objects.get(id = memberSession.get('seq'))
        if not (oMember.level > 100):
            raise Exception

    except Exception,e :
        return False

    return True
