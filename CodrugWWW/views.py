# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context
from models import *
from controller import member
from controller import board_free
from controller import timeline

'''
    Index page /
'''
def index(request):
    tpl = get_template('index.html')
    htmlData = tpl.render( Context() )

    #htmlData = "Hello world."


    return HttpResponse(htmlData)

