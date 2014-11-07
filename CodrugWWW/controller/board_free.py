# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context
from ..models import *


'''
    Freeboard write
    GET method 로 접근시 글쓰기 폼을 보여주며
    POST method 로 접근시 글쓰기 작업을 진행한다.
'''
def boardFree_write(request):

    if request.method == 'GET' :
        ctx = Context({

        })

        tpl = get_template('boardFreeWrite.html')
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
            category = Category.objects.get( boardNAME = 'free' )


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
    Freeboard list
'''
def boardFree_list(request, page = 1):
    if len(str(page)) == 0: page = 1
    category = Category.objects.filter(boardNAME='free')
    article = Board.objects.filter(category=category)

    ctx = Context({
        'page' : page,
        'boardName' : 'free',
        'article' : article
    })

    tpl = get_template('boardFreeList.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)


'''
    Freeboard detail

'''

def boardFree_detail(request, id):
    article = Board.objects.get(id)
    ctx=Context({
        'article':article
    })
    tpl = get_template('boardFreeDetail.html')
    htmlData= tpl.render(ctx)

    return HttpResponse(htmlData)

