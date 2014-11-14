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
    Archive write
    GET method 로 접근시 글쓰기 폼을 보여주며
    POST method 로 접근시 글쓰기 작업을 진행한다.
'''
def boardArchive_write(request):

    if request.method == 'GET' :

        if not request.session.get('member_login'):
            return HttpResponse( utils.scriptError(' 회원만 접근이 가능합니다. ', '/') )

        ctx = {}
        rContext = RequestContext( request )
        htmlData = render(request, 'boardArchiveWrite.html', ctx, context_instance = rContext)
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
            category = Category.objects.get( boardNAME = 'archive' )


            board_title = unicode( utils.cleanStr( request.POST.get('board_title') ) )
            board_content =  unicode( request.POST.get('board_content').strip() )

            if( len(board_title) == 0 or len(board_content) == 0):
                raise Exception

            ##---------------------------------------
            ## FILE UPLOAD
            ##---------------------------------------
            if 'board_file' in request.FILES:
                rFile = utils.fileUpload(request.FILES, 'board_file') # 리턴값 : (원본파일이름, 변환파일이름, 파일타입)
                if rFile[0] is not None:
                    try:
                        lastImage = File.objects.latest('id')
                        lastId = lastImage.id + 1 # 새로운 번호
                    except:
                        lastId = 1

                    oImage = File( seq = lastId, inFILE = rFile[0], outFILE = rFile[1], typeFILE = rFile[2])
                    oImage.save()
                else:
                    lastId = -1
            else:
                lastId = -1



            #--- FOR DEBUG --
            #print board_title
            #print board_content

            ##---------------------------------------
            ## BOARD INSERT
            ##---------------------------------------
            board = Board(title = board_title, content = board_content, category = category, memberID = oMember,
                          viewCount = 0, image_ref = lastId, extra = utils.getBoardExtraMessage(isConfirmed = False) )
            board.save()
        except Exception, e:
            HttpResponse( json.dumps( utils.sMessage( data = ' 작성중 오류가 발생하였습니다.', error = True)))


        return HttpResponse( json.dumps( utils.sMessage( data = 'archive' )))


    else:
        HttpResponse( json.dumps( utils.sMessage( data = ' 작성중 오류가 발생하였습니다.', error = True)))

'''
    Archive list
'''
def boardArchive_list(request, page = 1):
    if len(str(page)) == 0: page = 1
    category = Category.objects.filter(boardNAME='archive')
    article = Board.objects.filter(category=category).order_by('-id')
    articleCount = article.count()

    # 댓글 가공.
    for idx in range(0, len(article)):
        commentCount = Comment.objects.filter(category = category, articleID = article[idx]).count()
        article[idx].commentCount = commentCount


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


    ctx = {
        'page' : page,
        'boardName' : 'archive',
        'article' : article,
    }

    rContext = RequestContext( request )
    htmlData = render(request, 'boardArchiveList.html', ctx, context_instance = rContext)
    return HttpResponse(htmlData)


'''
    Archive detail

'''

def boardArchive_detail(request, id):
    article = Board.objects.get(id = id)
    comment = Comment.objects.filter(articleID = id)
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

    try:
        sExtra = json.loads(article.extra)
    except:
        sExtra = None

    print article

    ctx={
        'article':article,
        'comment':comment,
        'imgList':oImg,
        'fileList':oEtc,
    }
    rContext = RequestContext( request )
    htmlData = render(request, 'boardArchiveDetail.html', ctx, context_instance = rContext)
    return HttpResponse(htmlData)


'''
    Archive Comment
'''
def boardArchive_comment(request, articleId):

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

def boardArchive_delete(request, id):
    try:
        article = Board.objects.get(id = id)

        # 회원 정보가 존재하는지 확인. ( 없으면 exception )
        if not request.session['member_login']: raise Exception

        # 글 정보와 멤버 정보가 같은지 확인. ( 없으면 exception )
        if article.memberID.id != request.session['member_login'].get('seq') : raise Exception

        # 글 삭제.
        Board.delete(article)

        return redirect('board_archive_list')

    except Exception, e:
        return HttpResponse( utils.scriptError(' 게시물 삭제하는데 오류가 발생하였습니다. ') )



def boardArchive_modify(request, id):
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

