#!/usr/bin/python3

import serial
import sys
import time

def sendpkt(target,data,port=0):
	pkt = [0x03,len(data)+3,(target>>8)&0xFF,target&0xFF,port]+data
	pkt = bytearray(pkt)
	print("Waiting for CTS")
	while (not ser.getCTS()):
		if (ser.inWaiting() >= 2):
			parseResponse()
		time.sleep(0.0001)
	print("Got CTS")
	ser.write(pkt)

def parseResponse():
	atype = ord(ser.read(1))
	alen = ord(ser.read(1))
	payload=[]
	for i in range(alen):
		payload.append(ord(ser.read(1)))
	if atype == 0x50:
		print("Got ACK from {:x}{:x}".format(payload[0],payload[1]))
	if atype == 0x51:
		print("Got NACK from {:x}{:x}".format(payload[0],payload[1]))
	if atype == 0x52:
		print("Data from {:x}{:x}:{}".format(payload[0],payload[1],payload[2:]))
	

try: 
	ser = serial.Serial(sys.argv[1],baudrate=115200)
except:
	print("Usage: {} <port> <target_address>").format(sys.argv[0])


while True:
	sendpkt(int(sys.argv[2],16),[0xDE,0xAD])
	if (ser.inWaiting() >= 2):
		parseResponse()
	time.sleep(1)
