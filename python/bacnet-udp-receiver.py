#! /usr/bin/env python

import socket
import sys
from decode import bvlc
from decode import i_am


def udp_connect(ip, port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	#sock.bind(("10.50.80.255",47808))	
	sock.bind((ip,int(port)))

	while True:
		data, addr = sock.recvfrom(1024)
		print "message: ", data.encode('hex')
		#print "message: ", buf.encode('hex')
		decode(data)

def decode(buf):
	results = bytearray(buf)
	#if int(buf[7], 16) == 0:
	#print "I-am...", int(buf[0].encode('hex'),16)
	#print results[7]
	#print buf.encode('hex')
	#pass
	bvll_ = bvlc.bvll(results)
	npdu_ = bvlc.npdu(bvll_)
	apdu_ = bvlc.apdu(npdu_)
	iam_ =  i_am.iam(apdu_)
	print "I-am Device:", iam_
 
def main():
	udp_connect(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
	main()

""" End """
