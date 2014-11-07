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



'''
    QNA Write
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
                          viewCount = 0, extra = utils.getBoardExtraMessage( isConfirmed = False))
            board.save()
            print utils.getBoardExtraMessage()
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
    article = Board.objects.filter(category=category).order_by('-id')

    # sExtra 변환
    for idx in range(0, len(article)):
        sExtra = json.loads( article[idx].extra )
        article[idx].isConfirmed = sExtra['isConfirmed']


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
    })
    tpl = get_template('boardQnaList.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)

'''
QNA Detail
'''
def boardQna_detail(request, id):
    article = Board.objects.get(id = id)
    comment = Comment.objects.filter( articleID = article)

    # 파일이 존재하면 이미지, 기타파일 분류작업.
    oImg = []
    oEtc = []
    if article.image_ref > 0:
        oFile = File.objects.filter(id=article.image_ref)

        # 파일 분류작업
        for each in oFile:
            if re.search( r'\.(jpg|png|bmp)$', str(each.outFILE)):
                oImg.append(each)
            else:
                oEtc.append(each)



    sExtra = json.loads(article.extra)
    ctx=Context({
        'article':article,
        'comment':comment,
        'isConfirmed' : sExtra['isConfirmed'],
        'fileList':oEtc,
        'imgList':oImg,
        })

    tpl = get_template('boardQnaDetail.html')
    htmlData= tpl.render(ctx)

    return HttpResponse(htmlData)



'''
    QnA Comment
'''
def boardQna_comment(request, articleId):

    try:
        # 회원 인증
        member_login = request.session['member_login']
        if not member_login :
            return HttpResponse( json.dumps( utils.sMessage( error = True)) )


        # 각종 객체 가져옴.
        oMember = Member.objects.get( id = member_login['seq'] )
        oBoard = Board.objects.get( id = articleId)
        oCategory = oBoard.category

        # 데이터 받음
        board_content = unicode( utils.cleanStr( request.POST.get('board_content') ) )
        if len(board_content) == 0:
            raise Exception

        # Comment model
        oComment = Comment( category = oCategory, articleID = oBoard, upperComment = 255, content = board_content,
                            memberID = oMember)
        oComment.save()

        json_message = utils.sMessage( data = 1 )


    except Exception, e:
        print e
        json_message = utils.sMessage( data = '코멘트 쓰기에 실패하였습니다.', error = True)


    return HttpResponse( json.dumps(json_message) )

'''
    QnA 확인완료 작업
'''
def boardQna_closeArticle(request, articleId):

    try:
        # 회원 인증
        member_login = request.session['member_login']
        if not member_login :
            return HttpResponse( json.dumps( utils.sMessage( error = True)) )

        # 게시글 정보 가져옴
        oBoard = Board.objects.get( id = articleId )

        # 게시글 정보와 회원 소유주가 같은지 확인
        if oBoard.memberID != member_login['seq']:
            raise Exception




    except Exception, e:
        print e




