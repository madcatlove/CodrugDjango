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

'''
    과제 리스트 컨트롤러
'''

def assignment_list(request):
    if request.method == 'GET' :
        assignmentList = Assignment.objects.all().order_by('-id')
        # 파일이 존재하면 이미지, 기타파일 분류작업.
        oImg = []
        oEtc = []
        oPeople = []

        for idx in range(0, len(assignmentList)):
            assignmentList[idx].fileList = []
            assignmentList[idx].memberList = []
            assignmentList[idx].submitList = []


        for idx in range(0, len(assignmentList)):
            ## 파일 주입.
            if assignmentList[idx].image_ref > 0:
                try:
                    oFile = File.objects.filter(id = assignmentList[idx].image_ref )
                    for eFile in oFile:
                        assignmentList[idx].fileList.append( eFile.outFILE )
                except File.DoesNotExist, e:
                    assignmentList[idx].fileList = []

            ## 제출한사람 주입
            try:
                tempSubmit = Submit.objects.filter(assignmentID =assignmentList[idx].id )
                for eSubmit in tempSubmit:
                    try:
                        eSubmit.submitfile = File.objects.get( id = eSubmit.image_ref )
                    except:
                        eSubmit.submitfile = ''

                    assignmentList[idx].submitList.append( eSubmit )
                    assignmentList[idx].memberList.append( eSubmit.memberID )


            except Submit.DoesNotExist, e :
                assignmentList[idx].memberList = []
                assignmentList[idx].submitList = []



        rContext = RequestContext(request)
        ctx = {
            'aList' : assignmentList,
            'imgList' :oImg,
            'flieList':oEtc,
            }
        rend = render(request, 'assignment.html', ctx, context_instance=rContext)
        return HttpResponse( rend )

    # ---- DATA PROCESSING ---
    # 과제 제출 (POST)
    else:
        try:

            # 로그인이 안되어있으면??
            if not request.session['member_login'] :
                raise Exception

            assignment_content = utils.cleanStr( request.POST.get('assignment_content') )
            assignment_id = int( utils.cleanStr( request.POST.get('assignment_id')))

            if assignment_id < 0 :
                raise Exception
            if( len(assignment_content) == 0 ) :
                raise Exception

            # DB에 데이터 집어넣기
            member_seq = int( request.session['member_login'].get('seq') )
            member_email = utils.cleanStr( request.session['member_login'].get('email') )
            oMember = Member.objects.get( id = member_seq )

            # Assignment 에 쑤셔봄
            oAssignment = Assignment.objects.get(id = assignment_id)


            # 파일 업로드 과정
            if 'assignment_file' in request.FILES:
                rFile = utils.fileUpload(request.FILES, 'assignment_file') # 리턴값 : (원본파일이름, 변환파일이름, 파일타입)
                if rFile[0] is not None:
                    try:
                        lastImage = File.objects.latest('id')
                        lastId = lastImage.id + 1 # 새로운 번호
                    except:
                        lastId = 1

                    oImage = File( seq = lastId, inFILE = rFile[0], outFILE = rFile[1], typeFILE = rFile[2])
                    oImage.save()
                else:
                    raise Exception
            else:
                raise Exception


            # Submit 과제 제출.
            ####################

            # 이미 과제 제출한 내역이 있다면 업데이트 없으면 Insert
            try:
                oSubmit = Submit.objects.get( assignmentID = oAssignment, memberID = oMember)
                oSubmit.subtext = assignment_content
                if lastId > 0:
                    oSubmit.image_ref = lastId
                oSubmit.save()

            # 없을경우 새로운 INSERT
            except Submit.DoesNotExist, e:
                oSubmit = Submit(
                     assignmentID=oAssignment,
                     memberID=oMember,
                     subtext=assignment_content,
                     image_ref=lastId,
                )
                oSubmit.save()


            return redirect('assignment_list')
        except Exception, e:
            return HttpResponse(utils.scriptError("과제 제출에 실패하였습니다."))

















'''
      과제 생성 컨트롤러
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


