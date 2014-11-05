# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context
from ..models import *


def timeline(request,):
    ctx = Context({
    })
    content = {}
    content = Board.objects.all()
    ctx = Context({
        'content' : content
    })

    tpl = get_template('timeline.html')
    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)
