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


class FileException(Exception):
    def __init__(self, message):
        super(FileException, self).__init__(message)

class AssignmentException(Exception):
    def __init__(self, message):
        super(AssignmentException, self).__init__(message)