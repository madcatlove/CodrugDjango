from django.conf.urls import *
from django.contrib import admin

from CodrugWWW.views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CodrugDjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index, name = 'index'),

    ###################
    # Member
    url(r'^member/join', member.member_join, name = 'member_join'),
    url(r'^member/list', member.member_list, name = 'member_list'),
    url(r'^member/login', member.member_login, name = 'member_login'),

    ###################
    # QnA board
    url(r'^board/qna/$', qna_list, name = 'qna_list'),
    url(r'^board/qna/(?P<page>(\d*))?$', qna_list, name = 'qna_list'),

    ###################
    # Timeline
    url(r'^timeline/$', timeline.timeline, name='timeline'),

    ####################
    # Freeboard
    url(r'^board/free/(\d*)?$', board_free.boardFree_list, name='board_free_list'),
    url(r'^board/free/write', board_free.boardFree_write, name='board_free_write'),
    url(r'^board/free/detail/(\d*)$', board_free.boardFree_detail, name='board_free_list'),
)
