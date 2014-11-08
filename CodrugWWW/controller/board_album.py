# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context
import re
import math
from ..models import *


'''
    Album write
    GET method 로 접근시 글쓰기 폼을 보여주며
    POST method 로 접근시 글쓰기 작업을 진행한다.
'''
def boardAlbum_write(request):

    if request.method == 'GET' :
        ctx = Context({

        })

        tpl = get_template('boardAlbumWrite.html')
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
            category = Category.objects.get( boardNAME = 'album' )


            board_title = unicode( utils.cleanStr( request.POST.get('board_title') ) )
            board_content =  unicode( request.POST.get('board_content').strip() )

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
            print e


        return HttpResponse( json.dumps( utils.sMessage( data = 1 )))


    else:
        return HttpResponseForbidden();

'''
    Album list
'''
def boardAlbum_list(request, page = 1):
    if len(str(page)) == 0: page = 1
    page = int(page)

    category = Category.objects.filter(boardNAME='album')
    article = Board.objects.filter(category=category).order_by('-id')
    articleCount = article.count()

    # 파일이 존재하면 이미지, 기타파일 분류작업.
    oImg = []
    oEtc = []
    for x in article:
        if x.image_ref > 0:
            oFile = File.objects.filter(id=x.image_ref)
            # 파일 분류작업
            for each in oFile:
                if re.search( r'\.(jpg|png|bmp)$', str(each.outFILE)):
                    oImg.append(each)
                else:
                    oEtc.append(each)
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
    currentBlock = int( math.ceil( 1.0 * page / pageOffset ) )
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


    ctx = Context({
        'page' : page,
        'boardName' : 'album',
        'article' : article,
        'imgList' :oImg,
        'flieList':oEtc,

        'totalPage' : totalPage,
        'pageList' : pageList,
        })

    tpl = get_template('boardAlbumList.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)


'''
    Album detail

'''

def boardAlbum_detail(request, id):
    article = Board.objects.get(id = id)
    comment = Comment.objects.filter(articleID = id)
    # 조회수 1 증가
    article.viewCount += 1
    article.save()
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

    try:
        sExtra = json.loads(article.extra)
    except:
        sExtra = None

    print article

    ctx=Context({
        'article':article,
        'comment':comment,
        'imgList':oImg,
        'fileList':oEtc,
        })
    tpl = get_template('boardAlbumDetail.html')
    htmlData= tpl.render(ctx)

    return HttpResponse(htmlData)


'''
    Album Comment
'''
def boardAlbum_comment(request, articleId):

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


