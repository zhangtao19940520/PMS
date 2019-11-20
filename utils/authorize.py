#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "JentZhang"
from django.shortcuts import redirect


def check_login(func):
    """
    验证用户是否登录
    :param func:
    :return:
    """

    def inner(request, *args, **kwargs):
        user_info = request.session.get("user_info")
        if user_info:
            return func(request, *args, **kwargs)
        else:
            return redirect("/user/login")

    return inner
