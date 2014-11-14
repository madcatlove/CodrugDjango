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
import member
import board_free
import timeline



'''
    QNA Write
'''
def boardQna_write(request):

    if request.method == 'GET' :

        if not request.session.get('member_login'):
            return HttpResponse( utils.scriptError(' 회원만 접근이 가능합니다. ', '/') )

        ctx = {

        }
        rContext = RequestContext( request )
        htmlData = render(request, 'boardQnaWrite.html', ctx, context_instance=rContext)
        return HttpResponse(htmlData)

    elif request.method == 'POST':

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

            if( len(board_title) == 0 or len(board_content) == 0):
                raise Exception


            #--- FOR DEBUG --
            #print board_title
            #print board_content

            # data input
            board = Board(title = board_title, content = board_content, category = category, memberID = oMember,
                          viewCount = 0, extra = utils.getBoardExtraMessage( isConfirmed = False))
            board.save()
            print utils.getBoardExtraMessage()
        except Exception, e:
            HttpResponse( json.dumps( utils.sMessage( data = ' 작성중 오류가 발생하였습니다.', error = True)))


        return HttpResponse( json.dumps( utils.sMessage( data = 'qna' )))


    else:
        HttpResponse( json.dumps( utils.sMessage( data = ' 작성중 오류가 발생하였습니다.', error = True)))




'''
QNA list
'''

def boardQna_list(request, page = 1):
    if len(str(page)) == 0: page = 1
    page = int(page)

    category = Category.objects.filter(boardNAME='qna')
    article = Board.objects.filter(category=category).order_by('-id')
    articleCount = article.count()

    #########################
    # PAGING
    #########################
    countOffset = 10; # 한페이지에 보여줄 갯수
    pageOffset =   5; # 리스트에 보여줄 페이지 갯수
    startOffset = ( page -1 ) * countOffset
    article = article[startOffset:(startOffset+countOffset)] # 게시글 적절히 자름.

    pageList = []
    totalPage = int( math.ceil( 1.0 * articleCount / countOffset)) # 전체 페이지 갯수
    currentBlock = int(math.ceil( 1.0 * page / pageOffset ))
    startPageNum = (currentBlock-1) * pageOffset + 1

    if totalPage != 0:
        for s in range(0, pageOffset):
            pageList.append( int(startPageNum) )
            if startPageNum == totalPage:
                break
            startPageNum += 1
    else:
        totalPage = 1
        pageList.append(1)



    # sExtra 변환
    for idx in range(0, len(article)):
        sExtra = json.loads( article[idx].extra )
        article[idx].isConfirmed = sExtra['isConfirmed']
        article[idx].commentCount = Comment.objects.filter( articleID = article[idx] ).count()



    ctx = {
        'page' : page,
        'boardName' : 'qna',
        'article' : article,
        'totalPage' : totalPage,
        'countOffset' : countOffset,
        'articleCount' : articleCount,
        'pageOffset' : pageOffset,
        'pageList' : pageList,


    }
    rContext = RequestContext( request )
    htmlData = render(request, 'boardQnaList.html', ctx, context_instance=rContext)
    return HttpResponse(htmlData)

'''
QNA Detail
'''
def boardQna_detail(request, id):
    article = Board.objects.get(id = id)
    comment = Comment.objects.filter( articleID = article)
    # 조회수 1 증가
    article.viewCount += 1
    article.save()

    # 파일이 존재하면 이미지, 기타파일 분류작업.
    oImg = []
    oEtc = []
    if article.image_ref > 0:
        oFile = File.objects.filter(seq=article.image_ref)

        # 파일 분류작업
        for each in oFile:
            if re.search( r'\.(jpg|png|bmp)$', str(each.outFILE)):
                oImg.append(each)
            else:
                oEtc.append(each)



    sExtra = json.loads(article.extra)

    ctx = {
        'article':article,
        'comment':comment,
        'isConfirmed' : sExtra['isConfirmed'],
        'fileList':oEtc,
        'imgList':oImg,
        }

    rContext = RequestContext( request )
    htmlData = render(request, 'boardQnaDetail.html', ctx, context_instance=rContext)

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

        if oBoard.memberID.id != member_login['seq']:
            raise Exception

        getExtra = json.loads( oBoard.extra )
        getExtra['isConfirmed'] = True
        oBoard.extra = json.dumps( getExtra )
        oBoard.save()

        json_message = utils.sMessage( data = 1)


    except Exception, e:
        print e
        json_message = utils.sMessage( data = '질문 확인처리를 하지 못하였습니다.', error = True)


    return HttpResponse( json.dumps(json_message ))


def boardQna_delete(request, id):
    try:
        article = Board.objects.get(id = id)

        # 회원 정보가 존재하는지 확인. ( 없으면 exception )
        if not request.session['member_login']: raise Exception

        # 글 정보와 멤버 정보가 같은지 확인. ( 없으면 exception )
        if article.memberID.id != request.session['member_login'].get('seq') : raise Exception

        # 글 삭제.
        Board.delete(article)

        return redirect('board_qna_list')

    except Exception, e:
        print e
        return HttpResponse( utils.scriptError(' 게시물을 삭제하는데 오류가 발생하였습니다. ') )


'''
    QnA Modify
'''
def boardQna_modify(request, id):
    if  len(str(id)) == 0  :
        return HttpResponse( utils.scriptError(' 잘못된 접근입니다. ') )
    id = int(id)

    # ---- 게시글 수정 ----
    if request.method == 'POST':
        try:
            board = Board.objects.get( id = id )

            # 멤버 정보와 같은지 확인.( 작성자랑 맞는지 )
            if not request.session['member_login']:
                raise Exception

            if board.memberID.id != request.session['member_login'].get('seq') :
                raise Exception

            board_title =  utils.cleanStr( request.POST.get('board_title') )
            board_content = request.POST.get('board_content')

            if len(board_title) == 0 or len(board_content) == 0 :
                raise Exception

            board.title = board_title
            board.content = board_content
            board.save()

            return HttpResponse(json.dumps( utils.sMessage( data = '게시물을 정상적으로 수정하였습니다.', error = False) ))

        except Exception,e :
            print e
            return HttpResponse(json.dumps( utils.sMessage( data = '게시물 수정중 오류가 발생하였습니다.', error = True) ))


    # ---- 게시글 수정 뷰 ----
    else:
        try:
            board = Board.objects.get( id = id )

            # 멤버 정보와 같은지 확인.( 작성자랑 맞는지 )
            if not request.session['member_login']:
                raise Exception

            if board.memberID.id != request.session['member_login'].get('seq') :
                raise Exception

            # 게시글 뷰.
            rContext = RequestContext(request)
            ctx = {
                'board_title' : board.title,
                'board_content_json' : json.dumps(board.content),
                'boardNAME' : board.category.boardNAME,
                'id' : id,
            }
            htmlData = render(request, 'boardModify.html', ctx, context_instance=rContext)
            return HttpResponse(htmlData)

        except Exception,e :
            print 'exception', e
            return HttpResponse( utils.scriptError(' 잘못된 접근입니다. ') )


