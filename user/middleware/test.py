#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time：2020/12/22 14:17
# @Software：PyCharm
__author__ = "JentZhang"
from django.utils.deprecation import MiddlewareMixin


class Test(MiddlewareMixin):
    def process_request(self, request):
        print('test-request')

    def process_response(self, request, response):
        print('test-response')
        return response


class Test2(MiddlewareMixin):
    def process_request(self, request):
        print('test2-request')

    def process_response(self, request, response):
        print('test2-response')
        return response
