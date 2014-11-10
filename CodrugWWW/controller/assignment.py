# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from .. import utils

# Create your views here.
from django.template.loader import get_template
from django.template import Context
import re
import math
from ..models import *


def assignment_list(request):

    assignmentList = Assignment.objects.gets.all()

    tpl = get_template('assignment.html')
    ctx = Context({
        'aList' : assignmentList
    })


    htmlData = tpl.render( ctx )

    return HttpResponse(htmlData)