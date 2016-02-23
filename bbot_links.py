from bbot_feature import BBOT_FEATURE
import os
import re
import urllib2

LINKS_FILE="./links"

class BBOT_LINKS(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
		# line processor needs direct send
        self.sendchat=sendchat
        # file
        if not os.path.isfile(LINKS_FILE):
            self.linksfile=open(LINKS_FILE,"w")
        else:
            self.linksfile=open(LINKS_FILE,"r+")
            self.loadLinks()
        # commands
        self.myCommands=[]
        self.myCommands.append("!links")

    def loadLinks(self):
        self.links=[]
        for url in self.linksfile.read().split("\n"):
            if len(url.strip())>1:
                self.links.append(url.split(" ")[1])

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        try:
            if len(data)==1:
                subres=self.getlink()
            elif len(data)==2:
                subres=self.getlink(data[1].strip())
            results['data']=subres
        except Exception, err:
            results['error']=True
            results['data']="some links error has occured.. %s" % err
        finally:
            return results

    def moduleName(self):
        return "links"

    def moduleDescription(self):
        return "searches for param in links database or lists all of the links in database"

    def getlink(self,search=None):
		# log
		self.log("processing links request - search mode: %s" % (search if (search!=None) else "none"))
		if len(self.links)==0:
			self.log("empty links db")
			return "There are no links in the links database!"
        # full links request
		if search==None:
			self.log("returning all links")
			results=[]
			c=0
			for link in self.links:
				results.append("\x0303[link]\x03 "+link)
				c=c+1
				if c>6:
					results.append("\x0303[link]\x03 *SNIP*")
					break
			results.append("\x0303[link]\x03 Returned %i results" % len(self.links))
			return results
		else:
			self.log("returning subset of links")
			results=[]
			for link in self.links:
				if search in link:
					self.log("adding %s to results" % link)
					results.append("\x0303[link]\x03 "+link)
			sres="\x0303[link]\x03 Returned %i results" % len(results) if len(results)>0 else "\x0303[link]\x03 no results"
			results.append(sres)
			return results

    def lineProcessor(self,nick,data,channel):
		# log
		self.log("processing line")
		# add link
		if "http" in " ".join(data):
			self.log("http found in line")
			l=" ".join(data)[" ".join(data).find("http"):]
			self.addlinkShowTitle(nick,l[:l.find(" ") if (l.find(" ")>-1) else None],channel)

    def addlinkShowTitle(self,nick,url,channel):
        # log
        self.log("processing link")
		# validate
        if not re.compile('^http[s]?://(www.)?[a-zA-Z0-9_.=\/?&-]*$').match(url):
			return
		# display title
        self.displayTitle(url,channel)
        # update links if necessary
        if url in self.links:
			self.log("dupe link")
			return
		# log
        self.log("adding url: %s" % url)
		# add url to in memory urls
        self.links.append(url)
		# add url to db
        self.linksfile.write(nick+" "+url+"\n")
        self.linksfile.flush()

    def displayTitle(self,url,channel):
        # log
		self.log("displaying title for link: %s" % url)
		try:
			data=urllib2.urlopen(urllib2.Request(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24"})).read()
			t=data[data.lower().find("<title>")+7:]
			t=t[:t.lower().find("</title>")]
			if not len(t)>256:
				self.sendchat(channel,"URL [ %s ]" % t.strip())
		except urllib2.URLError:
			pass
