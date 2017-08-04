#!/usr/bin/env python
# -*- coding:utf-8 -*-
import nmaptask
"""
实现快速扫描随机生成的IPV6地址，并返回这些随机的IPV6真正接入公网的IPV6地址列表。供nmaptask调用
"""
scaninstance = None
def getObject():
    global scaninstance
    if scaninstance is None:
        scaninstance = FastScan()

    return scaninstance

class FastScan(object):
    def __init__(self):
        pass

    def do_scan(self):
        nm = nmaptask.getObject()
        nm.add_work(['2001:250:4401:2000::100', '2001:250:4401:2000::102','2001:250:4401:2000:6254:7e81:ed31:5353'])


def test():
    nm =nmaptask.getObject()
    nm.add_work(['2001:3::100','2001:3::101'])

if __name__ == '__main__':
    test()

