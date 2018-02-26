#! /usr/bin/env python

import socket
import sys

""" enter adapter IP address of BACnet device. if broadcast enter xxx.xxx.xxx.255 """
UDP_IP = sys.argv[1]
""" BACnet default port 47808 """
UDP_PORT = int(sys.argv[2])

INSTANCE_LOW = sys.argv[3]
INSTANCE_HIGH = sys.argv[4]

""" Type = 0x81 for BACnet/IP """
BVLC_TYPE = 0x81 

""" Function = 0x0b for original broadcast NPDU """
BVLC_FUNC = 0x0b

""" Length 2 bytes variable. Will be calculated later...  """
BVLC_LENGTH_H = 0x00 
BVLC_LENGTH_L = 0x00 

""" NPDU version = 0x01. Always 0x01 Ashrea 135-1995 """
NPDU_VER = 0x01

""" NPCI control octet = 0x20. bin = 100000. Bit 5 is set, means DNET-DLEN Hop Count are present, no expectation reply, priority normal """
NPCI = 0x20

""" Destination address = 65535 """
DNET_H = 0xff
DNET_L = 0xff

""" MAC layer address = 0, indicates a broadcast """
DADR = 0x00

""" Hop count = 255 """
HOPC = 0xff

""" APDU Type = 0x10, unconfirmed request """
APDU_TYPE = 0x10

""" APDU service = 0x08, who-is """
APDU_SERV = 0x08
 

def inst_low_bytes(inst):

	if (inst > 65535): 
		tag = 0x0b
		byte_1 = inst >> 16
		byte_2 = (inst >> 8) & 0xff
		byte_3 = inst & 0xff
		return [tag,byte_1,byte_2,byte_3]
	else:
		tag = 0x0a
		byte_1 = inst >> 8
		byte_2 = inst & 0xff	
		return [tag,byte_1,byte_2]
	

def inst_high_bytes(inst):

	if (inst > 65535): 
		tag = 0x1b
		byte_1 = inst >> 16
		byte_2 = (inst >> 8) & 0xff
		byte_3 = inst & 0xff
		return [tag,byte_1,byte_2,byte_3]
	else:
		tag = 0x1a
		byte_1 = inst >> 8
		byte_2 = inst & 0xff	
		return [tag,byte_1,byte_2]


def length_calc(ln):
	
		byte_1 = ln >> 8
		byte_2 = ln & 0xff	
		return [byte_1,byte_2]


INSTANCE_LOW_BYTES = inst_low_bytes(int(INSTANCE_LOW))
INSTANCE_HIGH_BYTES = inst_high_bytes(int(INSTANCE_HIGH))

""" BVLC, NPDU, APDU Header message """
BACNET_IP = [BVLC_TYPE,BVLC_FUNC,BVLC_LENGTH_H,BVLC_LENGTH_H,NPDU_VER,NPCI,DNET_H,DNET_L,DADR,HOPC,APDU_TYPE,APDU_SERV]

for i in range(0, len(INSTANCE_LOW_BYTES)):
	BACNET_IP.append(INSTANCE_LOW_BYTES[i])

for i in range(0, len(INSTANCE_HIGH_BYTES)):
	BACNET_IP.append(INSTANCE_HIGH_BYTES[i])

LENGTH_TOT = len(BACNET_IP)
LENGTH = length_calc(LENGTH_TOT)

BACNET_IP[2] = LENGTH[0]
BACNET_IP[3] = LENGTH[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.sendto(bytearray(BACNET_IP), (UDP_IP, UDP_PORT))
#print BACNET_IP
#print '[{}]'.format(', '.join(hex(x) for x in BACNET_IP))
	

""" End """








""" ******************************************** test ********************************************  """
 
"""
UDP_IP = "10.50.80.22" or "10.50.80.255"

INSTANCE_MIN_H = int(sys.argv[3]) >> 8
INSTANCE_MIN_L = int(sys.argv[3]) & 0xff
INSTANCE_MAX_H = int(sys.argv[4]) >> 8
NSTANCE_MAX_L = int(sys.argv[4]) & 0xff

#WHO-IS range 1200-1200 #MESSAGE = bytearray([0x81,0x0b,0x00,0x12,0x01,0x20,0xff,0xff,0x00,0xff,0x10,0x08,0x0a,INSTANCE_MIN_H,INSTANCE_MIN_L,0x1a,INSTANCE_MAX_H,INSTANCE_MAX_L])

MESSAGE = bytearray([0x81,0x0b,0x00,0x12,0x01,0x20,0xff,0xff,0x00,0xff,0x10,0x08,0x0b,0x00,INSTANCE_MIN_H,INSTANCE_MIN_L,0x1b,0x00,INSTANCE_MAX_H,INSTANCE_MAX_L])

"""

