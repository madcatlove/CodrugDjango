from django.db import models


'''
    Member Model
'''
class Member(models.Model):

    '''
        Member Field
    '''
    email = models.CharField(max_length = 150)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 30)
    image_url = models.CharField(max_length = 100, null= True, default='')

