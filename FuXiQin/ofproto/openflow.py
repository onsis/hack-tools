#!/usr/bin/python

"""
TODO:Defined   the  openflow  message  type
Author:SunXiaoTian
Time:2016/9/30 
"""
import sys
#sys.path.append('/usr/lib/pytohn2.7/dist-packages/')
sys.path

from  scapy.all import *

####################
# Data  Structures #
####################

#uint8_t => XByteField
#uint16_t => ShortFIeld,BitFieldLenField('name',None,16,length_of='varfield'),BitField('name',None,16)
#uint32_t => IntField,BitFieldLenField('name',None,32,length_of='varfield'),BitFieldLenField('name',None,32)

ofp_type = { #Immutable  message#
	     0:"OFPT_HELLO",
             1:"OFPT_ERROR",
             2:"OFPT_ECHO_REQUEST",
             3:"OFPT_ECHO_REPLY",
             4:"OFPT_EXPERIMENTER",
             # Switch configuration message #
             5:"OFPT_FEATURES_REQUEST",
             6:"OFPT_REATURES_REPLY",
             7:"OFPT_GET_CONFIG_REQUEST",
             8:"OFPT_GET_CONFIG_REPLY",
             9:"OFPT_SET_CONFIG",
             # Asynchronous  message #
             10:"OFPT_PACKET_IN",
             11:"OFPT_FLOW_REMOVED",
             12:"OFPT_PORT_STATUS",
             # Controller command  message #
             13:"OFPT_PACKET_OUT",
             14:"OFPT_FLOW_MOD",
             15:"OFPT_GROUP_MOD",
             16:"OFPT_PORT_MOD",
             17:"OFPT_TABLE_MOD",
             # Multipart  message #
             18:"OFPT_MULTIPART_REQUEST",
             19:"OFPR_MULTIPART_REPLY",
             # Barrier  message #
             20:"OFPT_BARRIER_REQUEST",
             21:"OFPT_BARRIER_REPLY",
             # Queue  Configuration  message #
             22:"OFPT_QUEUE_GET_CONFIG_REQUEST",
             23:"OFPT_QUEUE_GET_CONFIG_REPLY",
             #  Controller  role  change  request  message #
             24:"OFPT_ROLE_REQUEST",
             25:"OFPT_ROLE_REPLY",
             #  Asynchronous  message  configuration #
             26:"OFPT_GET_ASYNC_REQUEST",
             27:"OFPT_GET_ASYNC_REPLY",
             28:"OFPT_SET_ASYNC",
             # Meters  and  rate  limiters  configuration message #
             29:"OFPT_METER_MOD"
           }

ofp_error_type={
      0:"OFPET_HELLO_FAILED",
      1:"OFPET_BAD_REQUEST",
      2:"OFPET_BAD_ACTION",
      3:"OFPET_BAD_INSTRUCTION",
      4:"OFPET_BAD_MATCH",
      5:"OFPET_FLOW_MOD_FAILED",
      6:"OFPET_GROUP_MOD_FAILED",
      7:"OFPET_PORT_MOD_FAILED",
      8:"OFPET_TABLE_MOD_FAILED",
      9:"OFPET_QUEUE_OP_FAILED",
      10:"OFPET_SWITCH_CONFIG_FAILED",
      11:"OFPET_ROLE_REQUEST_FAILED",
      12:"OFPET_METER_MOD_FAILED",
      13:"OFPET_TABLE_FEATURES_FAILED",
      0xffff:"OFPET_EXPERIMENTER"
}

ofp_port_config={
		1<<0:"OFPPC_PORT_DOWN",
		1<<2:"OFPPC_NO_RECV",
		1<<5:"OFPPC_NO_FWD",
		1<<6:"OFPPC_NO_PACKET_IN"
		}

ofp_multipart_type = {
      0:"OFPMP_DESC",
      1:"OFPMP_FLOW",
      2:"OFPMP_AGGREGATE",
      3:"OFPMP_TABLE",
      4:"OFPMP_PORT_STATS",
      5:"OFPMP_QUEUE",
      6:"OFPMP_GROUP",
      7:"OFPMP_GROUP_DESC",
      8:"GROUP_FEATURES",
      9:"OFPMP_METER",
      10:"OFPMP_METER_CONFIG",
      11:"OFPMP_METER_FEATURES",
      12:"OFPMP_TABLE_FEATURES",
      13:"OFPMP_PORT_DESC",
      0Xffff:"OFPMP_EXPRIMENTER"
}

ofp_multipart_reply_flags = {
      1<<0:"OFPMP_REPLY_MORE"
}

ofp_config_flags = {
      0:"OFPC_FRAG_NORMAL",
      1<<0:"OFPC_FRAG_DROP",
      1<<1:"OFPC_FRAG_REASM",
      3:"OFPC_FRAG_MASK"
}

ofp_controller_role = {
      0:"OFPCR_ROLE_NOCHANGE",
      1:"OFPCR_ROLE_EQUAL",
      2:"OFPCR_ROLE_MASTER",
      4:"OFPCR_ROLE_SLAVE"
}
######################
#  openflow  header  #
######################


class  ofp_header(Packet):
	name = "openflow header"
	fields_desc=[XByteField("version",4),
		     ByteEnumField("type",0,ofp_type),
		     ShortField("length",8),
		     IntField("xid",1)
	                     ]


#####################
# openflow  message #
#####################


# No.1
#[header|error]
class  ofp_error(Packet):
                  name="openflow error message"
                  field_desc=[ShortEnumField("type",0,ofp_error_type),
		    ShortField("code",0),
		    StrFixedLenField("data",None,length=8),
		    ]
bind_layers(ofp_header,ofp_error,type=1)

#No.6
#[header|features_reply]
class ofp_features_reply(Packet):
                  name = "opeflow  features reply"
                  fields_desc=[BitField("datapath_id",None,64),
                                    BitField("n_buffers",None,32),
                                    XByteField("n_tables",0),
                                    XByteField("auxiliary_id",0),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    BitField("OFPC_FLOW_STATS",0,1),
                                    BitField("OFPT_TABLE_STATS",0,1),
                                    BitField("OFPT_PORT_STATS",0,1),
                                    BitField("OFPT_GROUP_STATS",0,1),
                                    BitField("OFPT_IP_REASM",0,1),
                                    BitField("OFPT_QUEUE_STATS",0,1),
                                    BitField("OFPT_PORT_BLOCKED",0,1),
                                    BitField("NOT DIFINED",0,22),
                                    BitField("reserved",0,32),
                                    ]
bind_layers(ofp_header,ofp_features_reply,type=6)

#No.8
#[ofp_header|ofp_get_config_reply]
#class ofp_get_config_reply(Packet):
 #                 name = "openflow get config reply"
#                  fields_desc = [
 #                 ]
#No.9
#[ofp_switch_config]
class ofp_switch_config(Packet):
                  name = "openflow switch config"
                  fields_desc = [ShortEnumField("flags",0,ofp_config_flags),
                                    ShortField("miss_send_len",0)
                                     ]
#No.18
#[multipart_request]
class ofp_multipart_request(Packet):
                  name = "openflow multipart request"
                  fields_desc = [ShortEnumField("type",0,ofp_multipart_type),
                                    ShortEnumField("flags",0,ofp_multipart_reply_flags),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    #XByteField("body",0),
                                    ]


#No.19
#[header|multipart_reply]
class ofp_multipart_reply(Packet):
                  name = "openflow multipart reply"
                  fields_desc = [ShortEnumField("type",0,ofp_multipart_type),
                                    ShortEnumField("flags",0,ofp_multipart_reply_flags),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    XByteField("body",0),
                                    ]
bind_layers(ofp_header,ofp_multipart_reply,type=19)


#No.24
#[ofp_role_request]
class ofp_role_request(Packet):
                  name = "openflow role request"
                  fields_desc = [IntEnumField("role",2,ofp_controller_role),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    XByteField("pad",0),
                                    BitField("generation_id",0,64)
                  ]
