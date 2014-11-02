from django.http import HttpResponse
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
    pass

'''
    Member Login page /member/login
'''
def member_login(request):
    pass

