#!/usr/bin/env python

"""
KD90 CPU Temperature Monitor

Parse CPU temperature in the KD90 box to avoid CPU burn.

Useage: ./KD90_temperature_monitor.py

Copyright (C) 2012   LIU Qi (liuqi82@gmail.com)

"""

import urllib
import time
from HTMLParser import HTMLParser

temp_list = []
check_interval = 1
alarm_temperature = 33


post_data = { "b0switch" : "1", \
	      "b1switch" : "1", \
	      "b2switch" : "1", \
	      "b3switch" : "1", \
	      "b4switch" : "1", \
	      "allswitch" : "4", \
	      "Apply" : "Submit" }

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if (tag == "input") and (attrs[0][1].find("cpu") != -1):
			# print "node label and temp:", attrs[0][1], attrs[2][1]
			print "Checking", attrs[0][1], "Temperature:", attrs[2][1]
			if attrs[2][1] == "NULL":
				return
			if int(attrs[2][1]) > alarm_temperature:
				print "Closing Board", attrs[0][1][1], \
				      "| The temperature of", "CPU", attrs[0][1][5], "is: ", attrs[2][1]
				post_data["b"+attrs[0][1][1]+"switch"] = "3"
				# print post_data
				encoded_data = urllib.urlencode(post_data)
				fout = urllib.urlopen("http://192.168.90.158/option.htm", encoded_data)

while True:
	f = urllib.urlopen("http://192.168.90.158/temp.htm")
	parser = MyHTMLParser()
	parser.feed(f.read())
	time.sleep(check_interval)
