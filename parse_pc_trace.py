#!/usr/bin/env python

"""
EJTAG PC Log Parser

Parse and dump the CPU program counter trace with function name
from EJTAG PC log file for Loongson processors

Useage: ./parse_pc_trace.py kernel_image log_file_name core_id

Copyright (C) 2012   LIU Qi (liuqi82@gmail.com)

TODO:
	1. Use hash table to avoid the redundant addr2line operation
	2. Support the application space parse
"""

import os
import sys

kernel_image = sys.argv[1]
log_file = sys.argv[2]
core_id = int(sys.argv[3])
dis_cmd = 'mips64el-linux-addr2line -f -e %s 0xffffffff%s'

addr_list = []

with open(log_file) as f:
	for line in f:
		addr_list.append(line.split())

print "%d cores in the log file." % len(addr_list[0]),
print "PC trace of core %d is as follows:" % core_id

last_pc = "xxxxxxxx"
for pcs_one_time in addr_list:
	if pcs_one_time[core_id] == last_pc:
		show_pc = "........"
	else:
		show_pc = pcs_one_time[core_id]
		show_pc_func = \
		os.popen(dis_cmd % (kernel_image, pcs_one_time[core_id])).readline()
	last_pc = pcs_one_time[core_id]
	print show_pc, show_pc_func,
