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


'''
    Album write
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
def boardFree_list(request, page = 1):
    if len(str(page)) == 0: page = 1
    category = Category.objects.filter(boardNAME='album')
    article = Board.objects.filter(category=category)

    ctx = Context({
        'page' : page,
        'boardName' : 'free',
        'article' : article,
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

