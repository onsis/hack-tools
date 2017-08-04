#!/usr/bin/env python
# -*- coding:utf-8 -*-

import schedule


mainschedule = None

#定时任务添加函数
def addschedule(event,day_of_week='0-7',hour='11',minute='57',second='0',id=''):
    global mainschedule
    if mainschedule is None:
        mainschedule = schedule.schedulecontrol()
    mainschedule.addschedule(event,day_of_week,hour,minute,second,id=id)

#定时任务初始化函数
def scheduleinit():
    import taskitem
    global mainschedule
    mainschedule = schedule.schedulecontrol()
    #nmap定时任务器
    mainschedule.addschedule(taskitem.tick,'0-7', '0-23', '0-59', '*/5')
    print 'init schedule'

if __name__ == '__main__':
    scheduleinit()
    while True:
        pass