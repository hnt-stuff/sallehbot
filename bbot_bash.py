from bbot_feature import BBOT_FEATURE
import urllib2
import BeautifulSoup
import HTMLParser
import random

BASHTOPURL='http://bash.org/?top'
BASHURL='http://bash.org/?random'

class BBOT_BASH(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
	# seed
	random.seed(None)
        # commands
        self.myCommands=[]
        self.myCommands.append("!bash")
        self.myCommands.append("!bashtop")

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
	if len(data)>1:
	    return results
	top=(data[0]==self.myCommands[1])
        try:

	    # log
	    self.log('grabbing bash')
	    bashdata=urllib2.urlopen(urllib2.Request(BASHTOPURL if top else BASHURL,headers={ "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24" }),timeout=6).read()
	    bsoup=BeautifulSoup.BeautifulSoup(bashdata)

	    main=bsoup.findAll('td',attrs={'valign':'top'})

	    quotes=main[0].findAll('p',attrs={'class':'quote'})
	    qtext=main[0].findAll('p',attrs={'class':'qt'})

	    ri=random.randint(0,len(quotes)-1)

	    qid=quotes[ri].find('b').contents[0]

	    qt=''

	    for tt in qtext[ri]:
		#if not type(tt) is BeautifulSoup.Tag:
		if type(tt) is BeautifulSoup.NavigableString:
		    qt=qt+str(tt)

	    qid=HTMLParser.HTMLParser().unescape(qid)
	    qt=HTMLParser.HTMLParser().unescape(qt)

	    # chat
	    res=[]
	    res.append("\x0309[bash quote]\x03 \x0310%s\x03" % qid)
	    for qtt in qt.split('\n'):
		res.append("\x0309[bash quote]\x03 \x0310%s\x03" % qtt)

            # display
            results['data']=res
        except Exception, err:
            results['error']=True
            results['data']="error: %s" % err
        finally:
            return results

    def moduleName(self):
        return "bash"

    def moduleDescription(self):
        return "displays a random selection from bash.org"

