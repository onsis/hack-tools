#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import nmap
import time

nmapinstance=None
def getObject():
    global nmapinstance
    if nmapinstance is None:
        nmapinstance=NmapTool()
    return nmapinstance
class NmapTool(object):
    def __init__(self):
        try:
            self.nm = nmap.PortScanner()
            self.params = '-6  -A   -Pn  -sC  -R -v  -O -T5'
        except nmap.PortScannerError:
            print('Nmap not found', sys.exc_info()[0])
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit(1)

    def scan(self,hosts='localhost',port='22-443',arguments='',extensionmission='0',callback=''):
        print hosts
        if callback == '':
            callback = self.callback_result
        orders = ''
        if port == '':
            orders += port
        else:
            orders = None
        try:
            if extensionmission == '0':
                print self.params
                scan_result = self.nm.scan(hosts=hosts,ports=orders,arguments=self.params)
                return callback(scan_result)
            else:
                print self.params+arguments
                scan_result = self.nm.scan(hosts=hosts,ports=orders,arguments=self.params+arguments)
                return callback(scan_result)
        except nmap.PortScannerError:
            print('Nmap not found', sys.exc_info()[0])
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit(1)


    def callback_result(self,scan_result):
        tmp = scan_result
        #print tmp['scan']
        for i in tmp['scan'].keys():
            host = i
            result = ''
            tmp = scan_result
            result = ''
            try:
                print tmp['scan'][host].keys()
                result = u"ip地址:%s   ......  %s\n" % (host, tmp['scan'][host]['status']['state'])
                if 'osmatch' in tmp['scan'][host].keys():
                    print tmp['scan'][host]['osmatch']

                    #result += u"系统信息 ： %s %s %s   准确度:%s  \n" % (
                    #str(tmp['scan'][host]['osclass']['vendor']), str(tmp['scan'][host]['osclass']['osfamily']),
                    #str(tmp['scan'][host]['osclass']['osgen']), str(tmp['scan'][host]['osclass']['accuracy']))
                    #写入数据库
                if 'tcp' in tmp['scan'][host].keys():
                    #print tmp['scan'][host]['tcp']
                    ports = tmp['scan'][host]['tcp'].keys()
                    print ports
                    for port in ports:
                        #print port
                        #print tmp['scan'][host]['tcp'][port]
                        portinfo = " port : %s  name:%s  state : %s  product : %s version :%s   \n" % (port, tmp['scan'][host]['tcp'][port]['name'],
                                                                                                                tmp['scan'][host]['tcp'][port]['state'],tmp['scan'][host]['tcp'][port]['product'],
                                                                                                                tmp['scan'][host]['tcp'][port]['version'])

                        print portinfo
                        result += portinfo
                        # 写入数据库
                elif 'udp' in tmp['scan'][host].keys():
                    ports = tmp['scan'][host]['udp'].keys()
                    for port in ports:
                        portinfo = " port : %s  name:%s  state : %s  product : %s  version :%s  \n" % (
                        port, tmp['scan'][host]['udp'][port]['name'], tmp['scan'][host]['udp'][port]['state'],
                        tmp['scan'][host]['udp'][port]['product'], tmp['scan'][host]['udp'][port]['version'])
                        result += portinfo
                        # 写入数据库
            except Exception, e:
                print e
            except IOError, e:
                print '错误IOError' + str(e)
            except KeyError, e:
                print '不存在该信息' + str(e)
            finally:
                return str(scan_result)

    def do_scan(self,hosts=[],ports=[],arguments=''):
        pass
        temp = ''
        for i in range(len(hosts)):

            if len(ports) <= i:
                result = self.scan(hosts=hosts[i], arguments=arguments)
                if result is None:
                    pass
                else:
                    temp += result
            else:
                result = self.scan(hosts=hosts[i], port=ports[i], arguments=arguments)
                if result is None:
                    pass
                else:
                    temp += result
        return temp

if __name__ == '__main__':
    tmp = NmapTool()
    host = ["2001:c68:300:40::81"]
    print "start scan"
    tmp.do_scan(host)