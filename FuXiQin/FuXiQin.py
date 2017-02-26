#!/usr/bin/python
"""
TODO:To establish the underlying data communication and  The OpenFLow packets to send and receive
Author:SunXiaoTian
Time:2016/6/30
"""

import	errno
import	functools
import	socket
import	Queue
import	time
import	sys

from    scapy	import *
from   threading   import  Timer
from   tornado   import  ioloop as ioloop
from   ofproto   import  openflow  as of
from   ofproto   import  ofp_handler as  ofp_handler
sys.path.append('.')


fd_map = {}
message_queue_map = {}

global ready
read = 0

handler = { 0:ofp_handler.handle_hello,
            1:ofp_handler.handle_error,
            2:ofp_handler.handle_echo_request,
            3:ofp_handler.handle_echo_reply,
            4:ofp_handler.handle_experimenter,
            5:ofp_handler.handle_features_request,
            6:ofp_handler.handle_features_reply,
            7:ofp_handler.handle_get_config_request,
            8:ofp_handler.handle_get_config_reply,
            9:ofp_handler.handle_set_config,
            10:ofp_handler.handle_packet_in,
            11:ofp_handler.handle_flow_removed,
            12:ofp_handler.handle_port_status,
            13:ofp_handler.handle_packet_out,
            14:ofp_handler.handle_flow_mod,
            15:ofp_handler.handle_group_mod,
            16:ofp_handler.handle_port_mod,
            17:ofp_handler.handle_table_mod,
            18:ofp_handler.handle_multipart_request,
            19:ofp_handler.handle_multipart_reply,
            20:ofp_handler.handle_barrier_request,
            21:ofp_handler.handle_barrier_reply,
            22:ofp_handler.handle_queue_get_config_request,
            23:ofp_handler.handle_queue_get_config_reply,
            24:ofp_handler.handle_role_request,
            25:ofp_handler.handle_role_reply,
            26:ofp_handler.handle_get_async_request,
            27:ofp_handler.handle_get_async_reply,
            28:ofp_handler.handle_set_async,
            29:ofp_handler.handle_merter_mod
          }
def handle_connection(connection,address):
    print ">>>connection",connection,address

def handle_message(address,fd,events):
    sock = fd_map[fd]
    if events & io_loop.READ:
        data = sock.recv(1500)
        if data == '':
            print ">>>Connection Dropped"
            io_loop.remove_handler(fd)
        if len(data) < 8:
            print ">>>not a openflow message"
        else:
            if len(data) >= 8:
                OFMessage = of.ofp_header(data[:8])
                body = data[8:]
            if OFMessage.type == 0 :
                print OFMessage.length
                msg = handler[0] (data)
                message_queue_map[sock].put(str(msg))
                msg1 = handler[5](data)
                message_queue_map[sock].put(str(msg1))
            elif OFMessage.type == 6:
                handler[6] (data,fd)
		msg = handler[18](data,13)
                message_queue_map[sock].put(str(msg))
                #msg1 = handler[9](data)
                #msg2= handler[20](data)
                #msg3 = handler[7](data)
                #msg = msg1/msg2/msg3
		#message_queue_map[sock].put(str(msg))
            else:
		#print OFMessage.type
                msg = handler[OFMessage.type] (data,fd)
		if msg != None:
			message_queue_map[sock].put(str(msg))
            io_loop.update_handler(fd,io_loop.WRITE)
    if events & io_loop.WRITE:
        try:
            next_msg = message_queue_map[sock].get_nowait()
        except Queue.Empty:
            #print "%s queue empty" % str(address)
            io_loop.update_handler(fd,io_loop.READ)
        else:
            #print 'sending "%s" to %s' % (of.ofp_header(next_msg).type,address)
            sock.send(next_msg)

def connection_manager(sock,fd,events):
    try:
        connection,address = sock.accept()
    except socket.error,e:
        if e.args[0] not in (errno.EWOULDBLOCK,errno.EAGAIN):
            raise
        return
    connection.setblocking(0)
    handle_connection(connection,address)
    fd_map[connection.fileno()] = connection
    connection_handler = functools.partial(handle_message,address)
    io_loop.add_handler(connection.fileno(),connection_handler,io_loop.READ)
    print ">>>connection_manager:new switch",connection.fileno(),connection_handler
    message_queue_map[connection] = Queue.Queue()

def create_sock(block):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.setblocking(block)
    return sock

if __name__ == '__main__':
    sock = create_sock(0)
    sock.bind(("",6653))
    sock.listen(6653)

    io_loop = ioloop.IOLoop.instance()
    callback = functools.partial(connection_manager,sock)
    print sock,sock.getsockname()
    io_loop.add_handler(sock.fileno(),callback,io_loop.READ)
    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
        print ">>>quit"
    
        #for time in timer_list.timer_list:
            #timer.cancel()
        #sys.exit(0)
