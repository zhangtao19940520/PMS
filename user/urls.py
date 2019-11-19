#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "JentZhang"

from django.conf.urls import url
from django.urls import path
from user import views

urlpatterns = [
    path(r'login', views.login),
    path(r'register', views.register),
    path(r'terms', views.terms),
    path(r'getimgcode', views.getimagecode),
    path(r'getvercode', views.getvercode),
]
