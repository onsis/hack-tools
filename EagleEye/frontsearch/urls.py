#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url

import search

urlpatterns = [
    url(r'^$', search.index, name='search'),
    url(r'^searchmain/$',search.searchmain,name='searchmain'),

]