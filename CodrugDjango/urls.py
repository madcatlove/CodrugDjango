# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.contrib import admin
from CodrugWWW.controller import board_qna, board_free, board_album, board_archive, assignment, upload, admin

from CodrugWWW.views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CodrugDjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', index, name = 'index'),
    url(r'^$', timeline.timeline, name = 'index'),

    ###################
    # Member
    url(r'^member/join', member.member_join, name = 'member_join'),
    url(r'^member/list', member.member_list, name = 'member_list'),
    url(r'^member/login', member.member_login, name = 'member_login'),
    url(r'^member/logout', member.member_logout, name = 'member_logout'),
    url(r'^member/modify', member.member_modify, name = 'member_modify'),

    ###################
    # Album board
    url(r'^board/album/(\d*)?$', board_album.boardAlbum_list, name = 'board_album_list'),
    url(r'^board/album/detail/(\d*)$', board_album.boardAlbum_detail, name = 'board_album_detail'),
    url(r'^board/album/write',board_album.boardAlbum_write, name='board_album_write'),
    url(r'^board/album/comment/(?P<articleId>\d*)$', board_album.boardAlbum_comment, name='board_album_comment'),
    ###################
    # Archive board
    url(r'^board/archive/(\d*)?$', board_archive.boardArchive_list, name = 'board_archive_list'),
    url(r'^board/archive/detail/(\d*)$', board_archive.boardArchive_detail, name = 'board_archive_detail'),
    url(r'^board/archive/write',board_archive.boardArchive_write, name='board_archive_write'),
    url(r'^board/archive/comment/(?P<articleId>\d*)$', board_archive.boardArchive_comment, name='board_archive_comment'),
    url(r'^board/archive/modify/(\d*)$', board_archive.boardArchive_modify, name='board_archive_modify'),
    url(r'^board/archive/delete/(\d*)$', board_archive.boardArchive_delete, name='board_archive_delete'),

    ###################
    # QnA board
    url(r'^board/qna/(\d*)?$', board_qna.boardQna_list, name = 'board_qna_list'),
    url(r'^board/qna/detail/(\d*)$', board_qna.boardQna_detail, name = 'board_qna_detail'),
    url(r'^board/qna/write',board_qna.boardQna_write, name='board_qna_write'),
    url(r'^board/qna/comment/(?P<articleId>\d*)$', board_qna.boardQna_comment, name='board_qna_comment'),
    url(r'^board/qna/close/(?P<articleId>\d*)$', board_qna.boardQna_closeArticle, name='board_qna_close'),
    url(r'^board/qna/modify/(\d*)$', board_qna.boardQna_modify, name='board_qna_modify'),
    url(r'^board/qna/delete/(\d*)$', board_qna.boardQna_delete, name='board_qna_delete'),


    ###################
    # Timeline
    url(r'^timeline/$', timeline.timeline, name='timeline'),

    ####################
    # Freeboard
    url(r'^board/free/(\d*)?$', board_free.boardFree_list, name='board_free_list'),
    url(r'^board/free/write', board_free.boardFree_write, name='board_free_write'),
    url(r'^board/free/detail/(\d*)$', board_free.boardFree_detail, name='board_free_list'),
    url(r'^board/free/comment/(?P<articleId>\d*)$', board_free.boardFree_comment, name='board_free_comment'),
    url(r'^board/free/delete/(\d*)$', board_free.boardFree_delete, name='board_free_delete'),
    url(r'^board/free/modify/(\d*)$', board_free.boardFree_modify, name='board_free_modify'),

    ####################
    # Assignment
    url(r'^assignment/$', assignment.assignment_list, name='assignment_list'),
    url(r'^assignment/write$', assignment.assignment_write, name = 'assignment_write'),
    url(r'^assignment/(?P<articleId>\d*)$', assignment.assignment_detail, name = 'assignment_detail'),

    ###################
    # Upload
    url(r'^file/upload$', upload.uploadFile, name = 'file_upload'),

    ###################
    # Admin
    url(r'^manage/$', admin.adminIndex, name = 'admin_index'),
    url(r'^manage/member/$', admin.adminMember, name = 'admin_member'),
    url(r'^manage/member/(?P<memberId>\d+)$', admin.adminMemberProc, name = 'admin_member_proc'),
    url(r'^manage/assignment/$', admin.adminAssignmentList, name = 'admin_assignment_list'),
    url(r'^manage/assignment/write/$', admin.adminAssignmentWrite, name = 'admin_assignment_write'),

    #########
    # FOR TEST
    url(r'^testMode/$', testUpload, name = 'testMode'),
    )
