#!/usr/bin/env python
# -*- coding:utf-8 -*-
import nmaptool
import datetime
from tasktool import TaskTool
nmapinstance=None
def getObject():
    global nmapinstance
    if nmapinstance is None:
        nmapinstance=NmapTask()
    return nmapinstance

class NmapTask(TaskTool):
    def __init__(self):
      super(NmapTask,self).__init__()
      self.nm = nmaptool.getObject()

    def task(self,req):
        print '执行任务中' + str(datetime.datetime.now())
        print '收到数据：%s' % req
        self.nm.do_scan([req],['22'])

if __name__ == '__main__':
    nm = NmapTask()
    nm.add_work(['2001:c68:300:40::81','2001:250:4401:2000::100'])
