#!/usr/bin/python
import	openflow     as  of
from    scapy.all    import *
import sys
sys.path


"""
TODO:Defined   the  openflow  message  type
Author:SunXiaoTian
Time:2016/9/30 
"""




sock_dpid={}

def handle_hello(data,*arg):
	msg=of.ofp_header(data)
	if msg.version==0x04:
		print ">>>OFPT_HELLO"
		return data
	else:
		print ">>>HELLO FAILED"
		return None

def handle_error(data,*arg):
	body = data[8:]
	print ">>>OFPT_ERROR"
	of.ofp_error(body).show()
	return  None


def handle_echo_request(data,*arg):
	print ">>>OFPT_ECHO_REQUEST"
	rmsg = of.ofp_header(data)
	msg = of.ofp_header(type=3,xid=rmsg.xid)
	return msg


def handle_echo_reply(data,*arg):
	print ">>>OFPT_ECHO_REPLY"
	return None

def handle_experimenter(data,*arg):
	pass

def handle_features_request(data,*arg):
	print ">>>OFPT_FEATURES_REQUEST"
	msg = of.ofp_header(type=5)
	return  msg

def handle_features_reply(data,fd):
	print ">>>OFPT_FEATURES_REPLY"
	body = data[8:]
	msg = of.ofp_features_reply(body[0:24])
	sock_dpid[fd] = msg.datapath_id
	#print hex(msg.datapath_id)
	#print msg.n_buffers
	#print msg.n_tables
	return None

def handle_get_config_request(data,*arg):
	print ">>>OFPT_GET_CONFIG_REQUEST"
	msg =of.ofp_header(type=7)
	return msg

def handle_get_config_reply(data,*arg):
	print ">>>OFPT_GET_CONFIG_REPLY"
	msg = handle_multipart_request(data,0)
	return msg

def handle_set_config(data,*arg):
	print ">>>OFPT_SET_CONFIG"
	msg = of.ofp_header(type=9,length=12)/of.ofp_switch_config(miss_send_len=0xffff)
	return msg

def handle_packet_in(data,*arg):
	print ">>>OFPT_PACKET_IN"
	return  None

def handle_flow_removed(data,*arg):
	pass

def handle_port_status(data,*arg):
	print ">>>OFPT_PORT_STATUS"
	return None

def handle_packet_out(data,*arg):
	pass

def handle_flow_mod(data,*arg):
	pass

def handle_group_mod(data,*arg):
	pass

def handle_port_mod(data,*arg):
	pass

def handle_table_mod(data,*arg):
	pass

def handle_multipart_request(data,type):
	print ">>>OFPT_MULTIPART_REQUEST:"+ "%s" %(of.ofp_multipart_type[type])
	msg = of.ofp_header(type=18,length=16,xid=4)/of.ofp_multipart_request(type=type,flags=(1<<0))
	return msg

def handle_multipart_reply(data,*arg):
	body = data[8:]
	msg = of.ofp_multipart_reply(body[0:])
	print ">>>OFPT_MULTIPART_REPLY:" +"%s" % (of.ofp_multipart_type[msg.type])
	#print msg.type
	if msg.type == 13:
		return handle_set_config(data)/handle_get_config_request(data)
	elif msg.type == 0:
		return handle_role_request(data)

def handle_barrier_request(data,*arg):
	print ">>>OFPT_BARRIER_REQUEST"
	msg = of.ofp_header(type=20)
	return msg

def handle_barrier_reply(data,*arg):
	print ">>>OFPT_BARRIER_REPLY"
	return None

def handle_queue_get_config_request(data,*arg):
	pass

def handle_queue_get_config_reply(data,*arg):
	pass

def handle_role_request(data,*arg):
	print ">>>OFPT_ROLE_REQUEST"
	msg = of.ofp_header(type=24,length=24)/of.ofp_role_request(role=2)
	return msg

def handle_role_reply(data,*arg):
	print ">>>OFPT_ROLE_REPLY"
	return  None

def handle_get_async_request(data,*arg):
	pass

def handle_get_async_reply(data,*arg):
	pass

def handle_set_async(data,*arg):
	pass

def handle_merter_mod(data,*arg):
	pass
