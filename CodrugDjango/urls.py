# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.contrib import admin
from CodrugWWW.controller import board_qna

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
    url(r'^member/logout', member.member_logout, name = 'member_logout'),
    ###################
    # Album board
    url(r'^board/album/(\d*)?$', board_qna.boardQna_list, name = 'board_album_list'),
    url(r'^board/album/detail/(\d*)$', board_qna.boardQna_detail, name = 'board_album_detail'),
    url(r'^board/album/write',board_qna.boardQna_write, name='board_album_write'),
    url(r'^board/album/comment/(?P<articleId>\d*)$', board_qna.boardQna_comment, name='board_album_comment'),
    ###################
    # Archive board
    url(r'^board/archive/(\d*)?$', board_qna.boardQna_list, name = 'board_archive_list'),
    url(r'^board/archive/detail/(\d*)$', board_qna.boardQna_detail, name = 'board_archive_detail'),
    url(r'^board/archive/write',board_qna.boardQna_write, name='board_archive_write'),
    url(r'^board/archive/comment/(?P<articleId>\d*)$', board_qna.boardQna_comment, name='board_archive_comment'),
    ###################
    # QnA board
    url(r'^board/qna/(\d*)?$', board_qna.boardQna_list, name = 'board_qna_list'),
    url(r'^board/qna/detail/(\d*)$', board_qna.boardQna_detail, name = 'board_qna_detail'),
    url(r'^board/qna/write',board_qna.boardQna_write, name='board_qna_write'),
    url(r'^board/qna/comment/(?P<articleId>\d*)$', board_qna.boardQna_comment, name='board_qna_comment'),
    url(r'^board/qna/close/(?P<articleId>\d*)$', board_qna.boardQna_closeArticle, name='board_qna_close'),
    ###################
    # Timeline
    url(r'^timeline/$', timeline.timeline, name='timeline'),

    ####################
    # Freeboard
    url(r'^board/free/(\d*)?$', board_free.boardFree_list, name='board_free_list'),
    url(r'^board/free/write', board_free.boardFree_write, name='board_free_write'),
    url(r'^board/free/detail/(\d*)$', board_free.boardFree_detail, name='board_free_list'),
    url(r'^board/free/comment/(?P<articleId>\d*)$', board_free.boardFree_comment, name='board_free_comment'),
    )
