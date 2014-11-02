# -*- coding: utf-8 -*-
from django.db import models


class Member(models.Model):

    email = models.CharField(max_length = 150)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 30)
    image_url = models.CharField(max_length = 100, null= True, default='')

