#!/usr/bin/python3

import serial
import sys
import time
import json

pos = [0,0]
last = time.time()
log = open("msg.log","a")

def getpos():
	global pos
	msg = json.loads(sys.stdin.readline())
	if msg["class"] != "TPV":
		return
	try:
		pos = [msg["lon"],msg["lat"]]
	except:
		pos = [0,0]
	
		

def sendpkt(target,data,port=0):
	pkt = [0x03,len(data)+3,(target>>8)&0xFF,target&0xFF,port]+data
	pkt = bytearray(pkt)
	print("Waiting for CTS")
	while (not ser.getCTS()):
		while (ser.inWaiting() >= 2):
			parseResponse()
	print("Got CTS")
	ser.write(pkt)

def parseResponse():
	atype = ord(ser.read(1))
	alen = ord(ser.read(1))
	payload=[]
	for i in range(alen):
		payload.append(ord(ser.read(1)))
	if atype == 0x50:
		print("Got ACK from {:x}{:x} at {}".format(payload[0],payload[1],pos))
		log.write("ACK;{:x};{};{}\n".format(payload[1],pos[0],pos[1]))
	if atype == 0x51:
		print("Got NACK from {:x}{:x} at {}".format(payload[0],payload[1],pos))
		log.write("NACK;{:x};{};{}\n".format(payload[1],pos[0],pos[1]))
	if atype == 0x52:
		print("Data from {:x}{:x}:{} at {}".format(payload[0],payload[1],payload[2:],pos))
		log.write("DATA;{:x};{};{}\n".format(payload[1],pos[0],pos[1]))
	log.flush()
	

try: 
	ser = serial.Serial(sys.argv[1],baudrate=115200)
except:
	print("Usage: {} <port>").format(sys.argv[0])


while True:
	sendpkt(0x0030,[0xDE,0xAD])
	while (ser.inWaiting() >= 2):
		parseResponse()
	for i in range(20):
		time.sleep(0.05)
		getpos()
