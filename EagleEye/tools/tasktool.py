#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threadtool
import datetime

class TaskTool(object):
    def __init__(self):
        self.threadpool = threadtool.ThreadTool()
        self.threadpool.add_task(self.task)

    def task(self,req):
        print '执行任务中'+str(datetime.datetime.now())
        print '收到数据：%s' %req

    def add_work(self,work):
        self.threadpool.push(work)


if __name__ == '__main__':
    task = TaskTool()
    task.add_work([1,2,3,4,5])

