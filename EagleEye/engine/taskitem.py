#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tools import fastscan
def tick():
    print "do fastscan"
    temp = fastscan.getObject()
    temp.do_scan()