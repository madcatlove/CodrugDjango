# -*- coding: utf-8 -*-
__author__ = 'madcat'


'''
    Custom Exception class
'''
class MemberException(Exception):
    def __init__(self, message):
        super(MemberException, self).__init__(message)


class BoardException(Exception):
    def __init__(self, message):
        super(BoardException, self).__init__(message)