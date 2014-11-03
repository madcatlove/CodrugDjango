from django.conf.urls import patterns, include, url
from django.contrib import admin

from CodrugWWW.views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CodrugDjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index, name = 'index'),

    url(r'^member/join', member_join, name = 'member_join'),
    url(r'^member/list', member_list, name = 'member_list'),

    url(r'^board/qna/$', qna_list, name = 'qna_list'),
    url(r'^board/qna/(?P<page>(\d*))?$', qna_list, name = 'qna_list'),
    # url(r'^admin/', include(admin.site.urls)),
)
