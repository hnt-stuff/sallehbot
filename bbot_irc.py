#!/usr/bin/python

# bbotv1 (sally bot)
# by rage
# thanks to cocainbiceps/mush/stumper and the rest of you mofos from BH/DEFCON 2013 we now have sally bot! 
# 
# Hey Sally! Getta loadah little Johnny son-ava-bitch over here writing some bots n' shit

import socket
import time
import threading

LOGFILE="./irc.log"
CONNECT_WAIT=5

class BBOT_IRC:
	def __init__(self):
		# status
		self.connected=False
		# personal
		self.nick="sallybottest"
		self.nickpass="dasekret"
		self.user="sallyuser"
		self.email="sallehbot0@salleh.net"
		self.namerequest=False
		self.haveops=False
		self.lastnametime=0
		# network
		self.server="irc.freenode.com"
		self.serverport=6667 # add ssl support
		self.channels=[]
		self.channels.append("#theroom")
		self.fixmepw="optionalroomkey"
		self.sock=None
		# namelist
		self.namelist={}
		# handler interface
		self.handlerProc=None
		# log
		self.logfile=open(LOGFILE,"a")

	def start(self):
		# start connection
		while not self.connected:
			# connect
			self.connect()
			# start messageloop
			self.messageloop()
			# wait
			time.sleep(CONNECT_WAIT)

	def connect(self):
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.log("connecting to %s on port %i" % (self.server,self.serverport))
		self.sock.connect((self.server,self.serverport))
		self.connected=True
		# initial server auth
		self.ircauth()
		# wait after auth before join
		time.sleep(4)
		# join channels
		self.joinchans()

	def ircauth(self):
		time.sleep(2)
		self.sock.send("user %s %s %s %s\n" % (self.user,self.user,self.email,self.user))
		time.sleep(2)
		self.sock.send("nick %s\n" % self.nick)
		time.sleep(8)
		self.sock.send("PRIVMSG nickserv :identify %s\n" % self.nickpass)
		#self.sock.send("MODE %s +x\n" % self.nick)

	def joinchans(self):
		for chan in self.channels:
			# log
			self.log("joining channel: "+chan)
			self.sock.send("JOIN %s %s\n" % (chan,self.fixmepw))
			time.sleep(1)
			self.sock.send("PRIVMSG chanserv :op %s %s" % (chan,self.nick))
			time.sleep(1)

	def messageloop(self):
		while True:
			readbuffer=self.sock.recv(1024)
			if len(readbuffer) <= 0:
				break
			else:
				# parse
				messagedata=readbuffer.split(" ")
				if messagedata[0].lower()=="ping":
					self.pong(messagedata[1:])
				elif messagedata[1].lower()=="privmsg":
					self.processmessage([messagedata[0]] + messagedata[2:])
				#elif len(messagedata) > 3 and len(messagedata[3])==1 and messagedata[4] in self.channels:
				elif len(messagedata) > 4 and messagedata[4] in self.channels:
					self.processchannelnames(messagedata[4:])
				else:
					self.log("implement handling for: " + " ".join(messagedata))

	def pong(self,ping):
		# log
		self.log("PONG "+"".join(ping))
		self.sock.send("PONG %s\n" % "".join(ping))

	def log(self,message):
		self.logfile.write("-[bbot irc log] * %s\n" % message)
		self.logfile.flush()

	def processmessage(self,message):
		# log
		self.log("processing message: " + " ".join(message))
		# check
		if message[1].lower()==self.nick:
			# handle pm
			self.handlechat(message[0],message[1],message[2:],ispm=True)
		elif message[1].lower() in self.channels:
			# handle chat
			self.handlechat(message[0],message[1],message[2:])

	def handlechat(self,sender,nickchannel,message,ispm=False):
		type="chat"
		if ispm:
			type="pm"
		# log
		self.log("%s received from %s data: %s" % (type,sender,message))
		# process command
		if ispm:
			self.log("ignoring pm")
		else:
			#self.processchatcommand(sender,nickchannel,message)
			if not self.handlerProc==None:
				self.handlerProc(sender,nickchannel,message)

	def sethandler(self,handler):
		self.handlerProc=handler

	def sendall(self,senddata):
		self.sock.sendall(senddata)

	def processchannelnames(self,messagedata):
		channel=messagedata[0]
		namelist=[]

		self.log("processchannelnames: %s" % "".join(messagedata))

		# first nick has : preceeding it
		nname=messagedata[1][1:]
		# handle first nick case
		if nname[0]=="@" or nname[0]=="%" or nname[0]=="+":
			if nname[0]=="@" and nname[1:].strip()==self.nick:
				self.haveops=True
			nname=nname[1:]
		namelist.append(nname)

		for name in messagedata[2:]:
			if name[0]=="@" or name[0]=="%" or name[0]=="+":
				if name[0]=="@" and name[1:].strip()==self.nick:
					self.haveops=True
				namelist.append(name[1:].strip())
			else:
				namelist.append(name.strip())

		# update namelist
		self.namelist[channel]=namelist

		# because this (should) occur only in response to a !roulette request we can trigger it here (NO!)
		if self.namerequest:
			# ignore non requested name updates
			self.namerequest=False
			# log
			self.log(["names for channel "+channel] + self.namelist[channel])
			if self.haveops:
				self.log("i have ops! channel: %s" % channel)
			else:
				self.log("i do not have ops! channel: %s" % channel)
			
