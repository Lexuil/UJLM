import serial
import struct
import time
import sys
import os
import Image


RESET = struct.pack("BB",0x50, 0xF0)
TAKE_PICTURE = struct.pack("BB",0x5A, 0xF0)
GET_SIZE = struct.pack("BB",0x5B, 0xF0)
SEND_PICTURE = struct.pack("BB",0x5C, 0xF0)
STOP = struct.pack("BB",0x5D, 0xF0)

class JPEGCamera:
	
	def __init__(self, port, baudRate = 38400):
	  sys.stderr.write("inicio de camara\n")
	  self.port = port
	  self.baudRate = baudRate
	  self.ser = serial.Serial(self.port, self.baudRate)

	
	def begin(self):
	  falg = self.ser.read(1);
	  while(falg != 'Y'):
	  	falg = self.ser.read(1);

	  check = self.ser.read(15)
	  sys.stderr.write(check)
	  check = self.ser.read(30)
	  #sys.stderr.write(check)
	  sys.stderr.write('\n')

	
	def reset(self):
	  self.ser.write(RESET)
	  check = self.ser.read(15)
	  sys.stderr.write(check)
	  ok = self.ser.read(2)
	  sys.stderr.write(ok)
	  instr = self.ser.read(25)
	  #sys.stderr.write(instr)
	  sys.stderr.write('\n')

	
	def takepicture(self):
	  self.ser.write(TAKE_PICTURE)
	  check = self.ser.read(15)
	  sys.stderr.write(check)
	  ok = self.ser.read(2)
	  sys.stderr.write(ok)
	  instr = self.ser.read(25)
	  #sys.stderr.write(instr)
	  sys.stderr.write('\n')

	
	def getsize(self):
	  self.ser.write(GET_SIZE)
	  check = self.ser.read(11)
	  sys.stderr.write(check)
	  ok = self.ser.read(2)
	  dataSize = struct.unpack("BB",self.ser.read(2))
	  sys.stderr.write(ok)
	  sys.stderr.write('\n')
	  sys.stderr.write(str(dataSize[0]))
	  sys.stderr.write(' ')
	  sys.stderr.write(str(dataSize[1]))
	  sys.stderr.write(' , ')
	  sys.stderr.write(str(dataSize[0] * 256 + dataSize[1]))
	  instr = self.ser.read(25)
	  #sys.stderr.write(instr)
	  sys.stderr.write('\n')
	  
	  
	def savePicture(self, filename):
	  sys.stderr.write("Saving picture ...\n")
	  self.ser.write(SEND_PICTURE)
	  check = self.ser.read(10)
	  sys.stderr.write(check)
	  dataSize = struct.unpack("BB",self.ser.read(2))

	  size = dataSize[0] * 256 + dataSize[1]

	  image = self.ser.read(size)

	  f = open(filename, 'wb')
	  f.write(image)
	  f.close()
	
	def show(self,filename):
	  sys.stderr.write("Showing ...\n")

          image = Image.open(filename)
	  image.show()