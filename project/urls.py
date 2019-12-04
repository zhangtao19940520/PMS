#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "JentZhang"

from django.conf.urls import url
from django.urls import path
from project import views

urlpatterns = [
    path(r'p_market', views.market),
    path(r'p_manage', views.manage),
    path(r'p_func', views.func),
    path(r'create_project', views.create_project),
    path(r'search_my_create_project', views.search_my_create_project),
    path(r'update_project_delete', views.update_project_delete),
]
