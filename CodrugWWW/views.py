from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template
from django.template import Context
from models import *

'''
    Index page /
'''
def index(request):
    tpl = get_template('index.html')
    htmlData = tpl.render( Context() )

    #htmlData = "Hello world."
    cMember = Member( email = 'k@k.net', password='1234', name = 'Lee' )
    cMember.save()
    return HttpResponse(htmlData)

'''
    Member join page /member/join
'''
def member_join(request):
    tpl = get_template('member_join.html')
    htmlData = tpl.render( Context() )

    return HttpResponse( htmlData )

'''
    Member Login page /member/login
'''
def member_login(request):
    pass

def member_list(request):
    tpl = get_template('members.html')
    htmlData = tpl.render( Context() )

    return HttpResponse( htmlData )



def qna_list(request, page = '1'):
    print page
    try:
        page = int(page)
    except ValueError:
        raise Http404()

    sParam = {
        'page' : page
    }

    tpl = get_template('qna.html')
    htmlData = tpl.render( Context(sParam) )

    return HttpResponse(htmlData)