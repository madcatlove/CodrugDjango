# -*- coding: utf-8 -*-
from django.db import models


#회원정보
class Member(models.Model):
    email = models.CharField(max_length = 150, unique=True)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 30)
    image_url = models.CharField(max_length = 100, null= True, default='')
    extra = models.TextField(null=True, default='')

#게시판 정보
class Category(models.Model):
    category = models.PositiveIntegerField()
    boardNAME = models.CharField(max_length=150)
    extra = models.CharField(max_length=150)

#통합게시판
class Board(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    #생성시간
    created=models.DateTimeField(auto_now_add=True)
    #수정시간
    updated=models.DateTimeField(auto_now=True)
    viewCount=models.PositiveIntegerField()
    memberID=models.ForeignKey(Member)
    extra=models.CharField(max_length=200)
    #게시판 분류
    category=models.ForeignKey(Category)


#파일관리
class File(models.Model):
    category = models.ForeignKey(Category)
    articleID = models.ForeignKey(Board)
    #변환 전 파일 ( 원본 파일 이름 )
    inFILE= models.CharField(max_length=200)
    #변환 후 파일 ( hashed 파일 이름 )
    outFILE= models.CharField(max_length=200, unique=True)

#댓글
class Comment(models.Model):
    category = models.ForeignKey(Category)
    articleID = models.ForeignKey(Board)
    #부모댓글
    upperComment = models.PositiveIntegerField()
    content = models.TextField()
    memberID = models.ForeignKey(Member)
    created=models.DateTimeField(auto_now_add=True)

#과제
class Assignment(models.Model):
    title = models.CharField(max_length = 150)
    content = models.TextField()
    deadline = models.DateTimeField()

#과제제출
class Submit(models.Model):
    assignmentID=models.ForeignKey(Assignment)
    #과제설명
    subtext = models.TextField()
    category = models.ForeignKey(Category)
    created=models.DateTimeField(auto_now_add=True)
