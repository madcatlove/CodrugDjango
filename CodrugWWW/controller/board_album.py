# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
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

        if not request.session.get('member_login'):
            return HttpResponse( utils.scriptError(' 회원만 접근이 가능합니다. ', '/') )

        ctx = {
        }
        rContext = RequestContext(request)
        htmlData = render( request, 'boardAlbumWrite.html', ctx, context_instance = rContext)

        return HttpResponse( htmlData )


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

            if( len(board_title) == 0 or len(board_content) == 0):
                raise Exception

            ##---------------------------------------
            ## FILE UPLOAD ( Processing Multiple uploads )
            ##---------------------------------------
            fileList = request.FILES.getlist('board_file')

            # 파일 리스트가 0 개가 아니라면 업로드 처리.
            if len(fileList) != 0:
                # 최근 이미지 번호를 가져와 +1 ( 없으면 1로 설정 )
                try:
                    lastImage = File.objects.latest('id')
                    lastId = lastImage.id + 1
                except :
                    lastId = 1

                # 파일 업로드 처리.
                for fileData in fileList:
                    rFile = utils.fileUploadSingle( fileData ) # 리턴값 : (원본파일이름, 변환파일이름, 파일타입)
                    if rFile[0] is not None:
                        oImage = File( seq = lastId, inFILE = rFile[0], outFILE = rFile[1], typeFILE = rFile[2])
                        oImage.save()
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


        return HttpResponse( json.dumps( utils.sMessage( data = 'album' )))


    else:
        HttpResponse( json.dumps( utils.sMessage( data = ' 작성중 오류가 발생하였습니다.', error = True)))

'''
    Album list
'''
def boardAlbum_list(request, page = 1):
    if len(str(page)) == 0: page = 1
    page = int(page)

    category = Category.objects.filter(boardNAME='album')
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


    # 댓글 가공.
    for idx in range(0, len(article)):
        commentCount = Comment.objects.filter(category = category, articleID = article[idx]).count()
        article[idx].commentCount = commentCount

    # 게시물에 이미지 정보 주입.
    for idx in range(0, len(article)):
        if article[idx].image_ref > 0 :
            fileList = File.objects.filter( seq = article[idx].image_ref )
            article[idx].fileList = fileList



    ctx = {
        'page' : page,
        'boardName' : 'album',
        'article' : article,



        'totalPage' : totalPage,
        'pageList' : pageList,
        }

    rContext = RequestContext( request )
    htmlData = render(request, 'boardAlbumList.html', ctx, context_instance = rContext)
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

    ctx={
        'article':article,
        'comment':comment,
        'imgList':oImg,
        'fileList':oEtc,
        }
    rContext = RequestContext( request )
    htmlData = render(request, 'boardArchiveList.html', ctx, context_instance = rContext)
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


