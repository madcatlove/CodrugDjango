
# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render

from .. import utils, exceptions

# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
import re
from ..models import *


def adminIndex(request):
    ctx = {

    }
    rContext = RequestContext(request)
    htmlData = render(request, 'include/admin_layout.html', ctx, context_instance=rContext)

    return HttpResponse(htmlData)