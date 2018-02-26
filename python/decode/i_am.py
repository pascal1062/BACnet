#! /usr/bin/env python

def iam(buf):
	
	service = buf[0]
	tag = buf[1]
	tag_class = -1
	tag_num = -1
	tag_length = -1

	if (service == 0):
		""" Unconfirmed service = 0. meaning: I-am """
		tag_num = tag>>4
		tag_length = tag&0x07		
		tag_class = (tag>>3)&1
		#return tag_class
		if ((tag_class == 0) and (tag_num == 0x0c) and (tag_length == 0x04)):
			""" 4 bytes containing object type and object instance """	
			obj_ref = [buf[2],buf[3],buf[4],buf[5]]	
			hex_str = ''.join(format(x, '02x') for x in obj_ref)	
			obj_type = int(hex_str,16)>>22		
			obj_inst = int(hex_str,16)&0x3fffff		
			return obj_inst

#End
