"""
Sally's best friend Donna helps with utility chat functions. Most command functionality will be handled by DONNA via feature implementations.

Donna handles all "chat" features which form the basis for all functionality for sally bot
"""

import sys
import time
from bbot_facts import BBOT_FACTS
from bbot_boobs import BBOT_BOOBS
from bbot_links import BBOT_LINKS
from bbot_google import BBOT_GOOGLESEARCH
from bbot_randombagcheck import BBOT_RANDOMBAGCHECK
from bbot_sandwich import BBOT_SANDWICH
from bbot_urbandictionary import BBOT_URBANDICTIONARY
from bbot_geolocation import BBOT_GEOLOCATION
from bbot_bash import BBOT_BASH

LOGFILE="./donna.log"

SEND_DELAY=2
SEND_THRESH=3

class BBOT_DONNA:
	def __init__(self,sendchat,sendraw):
		  # log
		  self.logfile=open(LOGFILE,"a")
		  # sendchat
		  self.sendchat=sendchat
		  # features
		  self.features=[] 
		  # features implementation classes
		  self.facts=BBOT_FACTS(sendchat)
		  self.boobs=BBOT_BOOBS(sendchat)
		  self.links=BBOT_LINKS(sendchat)
		  self.google=BBOT_GOOGLESEARCH(sendchat)
		  self.bagcheck=BBOT_RANDOMBAGCHECK(sendchat,sendraw)
		  self.sandwich=BBOT_SANDWICH(sendchat)
		  self.ud=BBOT_URBANDICTIONARY(sendchat)
		  self.ip=BBOT_GEOLOCATION(sendchat)
		  self.bash=BBOT_BASH(sendchat)

		  # init features
		  self.regComamnd(self.facts.getCommands(),self.facts.getHandler(),self.facts.moduleDescription())
		  self.regComamnd(self.boobs.getCommands(),self.boobs.getHandler(),self.boobs.moduleDescription())
		  self.regComamnd(self.links.getCommands(),self.links.getHandler(),self.links.moduleDescription())
		  self.regComamnd(self.google.getCommands(),self.google.getHandler(),self.google.moduleDescription())
		  self.regComamnd(self.bagcheck.getCommands(),self.bagcheck.getHandler(),self.bagcheck.moduleDescription())
		  self.regComamnd(self.sandwich.getCommands(),self.sandwich.getHandler(),self.sandwich.moduleDescription())
		  self.regComamnd(self.ud.getCommands(),self.ud.getHandler(),self.ud.moduleDescription())
		  self.regComamnd(self.ip.getCommands(),self.ip.getHandler(),self.ip.moduleDescription())
		  self.regComamnd(self.bash.getCommands(),self.bash.getHandler(),self.bash.moduleDescription())

	def regComamnd(self,commands,commandhandler,description):
		  regged={}
		  regged['commands']=commands
		  regged['handler']=commandhandler
		  regged['description']=description
		  # add to list
		  self.features.append(regged)
		  
	def process(self,nick,data,channel):
		# log
		self.log("processing data")
		# commands
		if len(data)==1 and (data[0]=="!commands" or data[0]=="!help"):
			self.sendchat(channel,"\x0307sallybot v2.0\x03 - \x0305sexytime edition!\x03")
			c=0
			for feature in self.features:
				self.sendchat(channel,"\x0305[command]\x03 \x0309%s\x03 - \x0311%s\x03" % (" ".join(feature['commands']),feature['description']))
				c=c+1
				if c>=SEND_THRESH:
					time.sleep(SEND_DELAY)
					c=0
		# links line processor handles non commandbased link handling
		self.log("calling line processor")
		self.links.lineProcessor(nick,data,channel)

		# features
		for feature in self.features:
			if data[0].lower() in feature['commands']:
				self.log("calling feature handler with description %s" % feature['description'])
				feature['handler'](nick,data,channel)
				# first feature that is able to handle a command gets it
				break

	def log(self,logdata):
		self.logfile.write("-[bbot donna log] * %s\n" % logdata)
		self.logfile.flush()

