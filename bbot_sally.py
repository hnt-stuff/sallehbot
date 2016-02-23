#!/usr/bin/python

# bbotv2 (sally bot)
# by rage
# thanks to cocainbiceps/mush/stumper and the rest of you mofos from BH/DEFCON 2013 we now have sally bot! 
# 
# Hey Sally! Getta loadah little Johnny son-ava-bitch over here writing some bots n' shit

from bbot_irc import BBOT_IRC
from bbot_donna import BBOT_DONNA
import time
import os
import sys
import random
import threading

NAMETIME_DELTA=5
SEND_THRESH=4
LOGFILE="./sally.log"
URLFILE="./urls"
LINKSFILE="./links"
WORD_THRESH=20

class BBOT_SALLY:
	def __init__(self):
		# seed
		random.seed(None)
		# irc
		self.irc=BBOT_IRC()
		# donna
		self.donna=BBOT_DONNA(self.sendchat,self.irc.sendall)
		# logging
		self.logfile=open(LOGFILE,"a")

		# roulette kick reasons
		self.reasons=[]
		self.reasons.append("*** has decided to stick his head in a zombie's mouth. MUNCH!")
		self.reasons.append("*** has bravely jumped onto a live grenade!")
		self.reasons.append("*** tried to kick it to sally. SALLY is NOT AMUSED!")
		self.reasons.append("a hobgoblin has kidnapped ***!")
		self.reasons.append("*** just told a ninja that he isn't stealthy. the ninja disagreed!")
		self.reasons.append("BOOM HEADSHOT!!!")
		self.reasons.append("*** slips on a banana peel and falls off the earth")
		# bagcheck reasons
		self.breasons=[]
		self.breasons.append("*** was followed home by a drone WITH LASERS!")
		self.breasons.append("*** suddenly grew a beard. *** now looks suspicious! TSA does not approve!")
		self.breasons.append("*** was caught with a bag of herr0n up the bunghole!")
		self.breasons.append("Someone thought *** said bomb. TSA DROP KICKS!")
		# sandwich ingredients
		self.ingredients=[]
		self.ingredients.append("spare lingerie")
		self.ingredients.append("dead hookers")
		self.ingredients.append("uncooked eggs")
		self.ingredients.append("boogers")
		self.ingredients.append("unicorn tears")
		self.ingredients.append("turds")
		# rain 
		self.rainkill=False
		self.lastrain=None
		self.rainnoted=False
		self.rainfail=[]
		self.rainfail.append("Chun-Lo NO RUV YOU NO MO")
		self.rainfail.append("YOU NO GO THERE!")
		self.raingood=[]
		self.raingood.append("The power of Chun-Lo has been RESTORED!!")
		self.raingood.append("Chun-Ro feels tingring in his nether legion. It is his MANA LESTORED!")
		self.raingood.append("Chun-Lo has finished training in the mountains of Sea-Men. His MANA is now RESTORED!")
		self.raingood.append("Chun-Lo was visited by three ghosts during the night..... His MANA is now RESTORED!")
		self.raingood.append("Chun-Lo has read Eat Pray Love. His MANA is now RESTORED!")
		self.raingood.append("Chun-Lo randomly trips into a pool. Its a mana pool! His MANA is now RESTORED!!")
		# keywords
		self.words={}
		self.notwords=[]
		self.notwords.append("the")
		self.notwords.append("and")
		self.notwords.append("it")
		self.notwords.append("its")
		self.notwords.append("or")
		self.notwords.append("sally_")
		self.notwords.append("you")
		self.notwords.append("me")
		self.notwords.append("lol")
		self.notwords.append("that")
		self.notwords.append("they")
		self.notwords.append("for")
		# seed
		random.seed()
	    
	def log(self,message):
		  self.logfile.write("-[bbot sally log] * %s\n" % message)
		  self.logfile.flush()

	def start(self):
		# irc process chat command interface
         self.irc.sethandler(self.processchatcommand)
         self.irc.start()

	def getnickfromhost(self,host):
		return host[1:host.find("!")]
	
	def processchatcommand(self,sender,channel,command):
		# log
		self.log("processing chat command: %s " % " ".join(command))
		nick=self.getnickfromhost(sender)
		ncommand=[]
		ncommand.append(command[0][1:].rstrip())

		# prep ncommand
		for c in command[1:]:
			ncommand.append(c.rstrip())

		# donna feature handler
		threading.Thread(target=self.donna.process(nick,ncommand,channel)).start()

		return
	
	def sendpm(self,to,pm):
		nick=self.getnickfromhost(to)
		self.irc.sendall("PRIVMSG %s :%s\n" % (nick,pm))

	def sendchat(self,channel,message):
		# log
		self.log("PRIVMSG %s :%s\n" % (channel,message))
		self.irc.sendall("PRIVMSG %s :%s\n" % (channel,message))

salleh=BBOT_SALLY()
salleh.start()
		
