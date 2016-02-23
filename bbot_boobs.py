from bbot_feature import BBOT_FEATURE
import os
import random
import re

BOOBS_FILE="./boobs"

class BBOT_BOOBS(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
	# seed
	random.seed(None)
        # file
        if not os.path.isfile(BOOBS_FILE):
            self.boobsfile=open(BOOBS_FILE,"w")
        else:
            self.boobsfile=open(BOOBS_FILE,"r+")
            self.loadBoobs()
        # commands
        self.myCommands=[]
        self.myCommands.append("!boobs")

    def loadBoobs(self):
        self.urls=[]
        for url in self.boobsfile.read().split("\n"):
            if len(url.strip())>1:
                self.urls.append(url)

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        subres=None
        try:
            if len(data)==1:
                subres=self.geturl()
            elif len(data)==2:
                subres=self.addurl(nick,data[1].strip())
            results['data']=subres
        except Exception, err:
            results['error']=True
            results['data']="some boob error has occured ;] NOM!! % s" % err
        finally:
            return results

    def moduleName(self):
        return "boobs"

    def moduleDescription(self):
        return "gives access to boobs database. given a URL as param will add to database"

    def addurl(self,nick,url):
		# parse url 
		if not 'http' in url:
			return

		if not re.compile('^http[s]?://(www.)?[a-zA-Z0-9_.=\/?&-]*$').match(url):
			return
		
		if url in self.urls:
			# send response
			return "I have seen those boobs before %s, so when you find some new ones please share!" % nick
		# log
		self.log("adding url: %s" % url)
		# add url to in memory urls
		self.urls.append(url)
		# add url to db
		self.boobsfile.write(url+"\n")
		self.boobsfile.flush()
		# send response
		return "Thanks for the boobies %s! <3" % nick

    def geturl(self):
		# log
		self.log("processing url request")
		if len(self.urls)==0:
			return "There are no boobs registered in the database! Add some boobs!!"
		else:
			ri=random.randint(0,len(self.urls)-1)
			return self.urls[ri]

