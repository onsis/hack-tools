#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
    urls.py
    Author:sxt
    Email:sxtttian@163.com
    Time:2017/1/13
    License:GPL-3.0,see LICENSE for more details
"""
from django.conf.urls import url

import views




urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^index/$',views.index,name = 'index'),
    url(r'^logout/$',views.logout,name = 'logout'),
]