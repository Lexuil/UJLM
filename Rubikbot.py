import serial
import struct
import time
import sys
import os
import Image


HOME = struct.pack("BB",0xFF, 0xF0)
INITIAL = struct.pack("BB",0xFE, 0xF0)
RESET = struct.pack("BB",0x50, 0xF0)
TAKE_PICTURE = struct.pack("BB",0x5A, 0xF0)
GET_SIZE = struct.pack("BB",0x5B, 0xF0)
SEND_PICTURE = struct.pack("BB",0x5C, 0xF0)
STOP = struct.pack("BB",0x5D, 0xF0)

class Rubikbot:
	
	def __init__(self, port, baudRate = 38400):
		sys.stderr.write("Esperado bot...\n")
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
		sys.stderr.write(check)

	def home(self):
		self.ser.write(HOME)
		check = self.ser.read(7)
		sys.stderr.write(check)
		ok = self.ser.read(5)
		sys.stderr.write(ok)
		instr = self.ser.read(25)
		sys.stderr.write(instr)

	def initial(self):
		self.ser.write(INITIAL)
		check = self.ser.read(7)
		sys.stderr.write(check)
		ok = self.ser.read(5)
		sys.stderr.write(ok)
		instr = self.ser.read(25)
		sys.stderr.write(instr)
	
	def calibratearm(self, arm, dir, val):
		dird = {"derecha":0x20,"izquierda":0x21,"medio":0x22,"atras":0x23,"adelante":0x24,"derecha1":0x25,"izquierda1":0x26,"medio1":0x27,"atras1":0x28,"adelante1":0x29}
		self.ser.write(struct.pack("BBBBB",0xFC ,arm ,dird[dir] ,val , 0xF0))
		check = self.ser.read(14)
		sys.stderr.write(check)
		ok = self.ser.read(5)
		sys.stderr.write(ok)
		instr = self.ser.read(25)
		sys.stderr.write(instr)
	
	def cara(self, val):
		self.ser.write(struct.pack("BBB",0xFB ,val , 0xF0))
		check = self.ser.read(9)
		sys.stderr.write(check)
		ok = self.ser.read(5)
		sys.stderr.write(ok)
		instr = self.ser.read(25)
		sys.stderr.write(instr)

	
	def movearm(self, dir):
		command = struct.pack("BBBB" ,0xFA ,ord(dir[0]) ,ord(dir[1]) , 0xF0)
		self.ser.write(command)
		check = self.ser.read(13)
		sys.stderr.write(check)
		ok = self.ser.read(4)
		sys.stderr.write(ok)
		instr = self.ser.read(25)
		sys.stderr.write(instr)

	
	def cam_reset(self):
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
	  
	  
	def savepicture(self, filename):
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

		ok = self.ser.read(4)
		sys.stderr.write(ok)
		instr = self.ser.read(25)
		#sys.stderr.write(instr)
		sys.stderr.write('\n')
	
	def show(self,filename):
		sys.stderr.write("Showing ...\n")

		image = Image.open(filename)
		image.show()