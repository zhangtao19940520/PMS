#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "JentZhang"

import os
import json
from django import template

register = template.Library()


@register.simple_tag
def left_is_active(request_url='', curr_url=''):
    """
    左菜单是否是选中状态
    :param request_url:
    :param curr_url:
    :return:
    """
    if request_url == curr_url:
        return 'layui-this'
    else:
        return ''
