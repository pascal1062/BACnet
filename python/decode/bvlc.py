#! /usr/bin/env python


def bvll(buf):

	if (len(buf) > 4):
		if (buf[0] == 0x81):	
			if (buf[1] == 0x0b):
				""" 0x0b original broadcast NDPU """
				""" return buffer less 4 first bytes """
				return buf[4:]
			else:
				return False
		else:
			return False
	else:
		return False


def npdu(buf):

	control = 0
	nsdu_bit7 = 0
	reserved_bit6 = 0
	destination_bit5 = 0
	reserved_bit4 = 0
	source_bit3 = 0
	reply_bit2 = 0
	priority_bit_1 = 0
	priority_bit_0 = 0
	dest_net_H = 0
	dest_net_L = 0
	dest_len = -1
	dest_adr = 0
	hop_count = -1

	if (buf[0] == 0x01):
		control = buf[1]
		nsdu_bit7 = (control>>7)&1
		reserved_bit6 = (control>>6)&1
		destination_bit5 = (control>>5)&1
		reserved_bit4 = (control>>4)&1
		source_bit3 = (control>>3)&1
		reply_bit2 = (control>>2)&1
		priority_bit_1 = (control>>1)&1
		priority_bit_0 = control&1
	else:
		return False

	if ((reserved_bit6 == 0) and (reserved_bit4 == 0)):
		if (control == 0):
			"""  control octet = 0. meaning: End of NPDU and beginning of APDU """		
			""" return buffer less 2 first bytes """
			return buf[2:]				
		elif (destination_bit5 == 1):
			""" destination bit is set. meaning: next bytes are destination network, length and Hop count """
			dest_net_H = buf[2]
			dest_net_L = buf[3]
			dest_len = buf[4]

			if (dest_len == 0):
				""" destination length is 0. meaning: indicates a broadcast. next byte is Hop count. This is end of NPDU and beginning of APDU  """
				hop_count = buf[5]	
				"""  return buffer less 6 first bytes """			
				return buf[6:]


def apdu(buf):

	apdu_type = buf[0]

	if (apdu_type == 0x10):
		"""  PDU =  0x10. meaning: unconfirmed resquest. Next bytes are related to Service Type  """
		"""  return buffer less the first byte """
		return buf[1:]		 


#End	



		

