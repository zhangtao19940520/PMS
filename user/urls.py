#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "JentZhang"

from django.conf.urls import url
from django.urls import path
from user import views

urlpatterns = [
    path(r'', views.index),
]
