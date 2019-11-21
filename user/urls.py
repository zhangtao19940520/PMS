#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "JentZhang"

from django.conf.urls import url
from django.urls import path
from user import views

urlpatterns = [
    path(r'login', views.login),
    path(r'logout', views.logout),
    path(r'register', views.register),
    path(r'terms', views.terms),
    path(r'forget', views.forget),
    path(r'edit_user', views.edit_user),
    path(r'edit_user_header', views.edit_user_header),
    path(r'getimgcode', views.getimagecode),
    path(r'getvercode', views.getvercode),
]
