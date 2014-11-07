# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context
import re
from ..models import *
import member
import board_free
import timeline

__author__ = 'bebop'

'''QNA Write
'''

def boardQna_write(request):

    if request.method == 'GET' :
        ctx = Context({

        })

        tpl = get_template('boardQnaWrite.html')
        htmlData = tpl.render( ctx )

        return HttpResponse(htmlData)
    elif request.method == 'POST':

        print request.POST

        try:
            # 회원 인증
            member_login = request.session['member_login']
            print member_login
            if not member_login :
                return HttpResponse( json.dumps( utils.sMessage( error = True)) )
            oMember = Member.objects.get( id = int(member_login['seq']) )


            # category id 가져옴.
            category = Category.objects.get( boardNAME = 'qna' )


            board_title = unicode( utils.cleanStr( request.POST.get('board_title') ) )
            board_content =  unicode( request.POST.get('board_content').strip() )



            #--- FOR DEBUG --
            #print board_title
            #print board_content

            # data input
            board = Board(title = board_title, content = board_content, category = category, memberID = oMember,
                          viewCount = 0)
            board.save()
        except Exception, e:
            print e


        return HttpResponse( json.dumps( utils.sMessage( data = 1 )))


    else:
        return HttpResponseForbidden();




'''
QNA list
'''

def boardQna_list(request, page = '1'):
    if len(str(page)) == 0: page = 1
    category = Category.objects.filter(boardNAME='qna')
    article = Board.objects.filter(category=category)
    sExtra = json.loads(article)

    # 리스트에서 각 게시글에 해당하는 댓글의 개수 출력하고 싶지만 좆같음 '....(3)' 이런 식
    # def count_comment():
    #     for each in article:
    #         comment = Comment.objects.filter(Comment.articleID == each.id)
    #         cComment = len(comment)
    #         return cComment
    # comment = Comment.objects.filter(Comment.articleID == )

    ctx = Context({
        'page' : page,
        'boardName' : 'qna',
        'article' : article,
        'sExtra':sExtra['isConfirmed']
    })
    tpl = get_template('boardQnaList.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)

'''
QNA Detail
'''


def boardQna_detail(request, id):
    article = Board.objects.get(id)
    comment = Comment.objects.filter(Comment.articleID == id)
    if article.image_ref > 0:
        oFile = File.objects.filter(id=article.image_ref)
        oImg=[]
        oEtc=[]
        for each in oFile:
            if re.search( r'\.(jpg|png|bmp)$', str(each.outFILE)):
                oImg.append(each)
            else:
                oEtc.append(each)
    else:
        oFile = []
        oImg=[]
        oEtc=[]

    sExtra = json.loads(article.extra)
    ctx=Context({
        'article':article,
        'comment':comment,
        'sExtra': sExtra['isConfirmed'],
        'fileList':oEtc,
        'imgList':oImg,
        })
    tpl = get_template('boardQnaDetail.html')
    htmlData= tpl.render(ctx)

    return HttpResponse(htmlData)

