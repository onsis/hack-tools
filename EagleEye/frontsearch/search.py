#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
    search.py
    Author:sxt
    Email:sxtttian@163.com
    Time:2017/1/13
    License:GPL-3.0,see LICENSE for more details
"""
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    username = request.COOKIES.get('username','')
    return render_to_response('search.html', {'data':''})

def searchmain(request):
    content = request.GET.get('searchcontent', '')

    page = request.GET.get('page', '0')
    username = request.COOKIES.get('username', '')
    content = content.replace(' ', '%20')
    return render_to_response('searchdetail.html', {'data': content, 'page': page, 'username': username})