# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import *
from controller import member
from controller import board_free
from controller import timeline

'''
    Index page /
'''
def index(request):

    ctx = {}
    rContext = RequestContext(request)
    rend = render(request, 'index.html', ctx , context_instance = rContext)

    return HttpResponse( rend )

