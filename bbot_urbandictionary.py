from bbot_feature import BBOT_FEATURE
import urllib2
import BeautifulSoup
import random

UDURL='http://www.urbandictionary.com/random.php'

class BBOT_URBANDICTIONARY(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
        # seed
        random.seed(None)
        # commands
        self.myCommands=[]
        self.myCommands.append("!ud")

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        # log
        self.log("UD reading urban dictionary")
        try:
            uddata=urllib2.urlopen(urllib2.Request(UDURL,headers={ "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24" })).read()
            udsoup=BeautifulSoup.BeautifulSoup(uddata)
            sinner=udsoup.findAll('div',attrs={'class':'inner'})
            wi=random.randint(0,len(sinner)-1)
            sword=sinner[wi].find('div',attrs={'class':'word'}).getText().encode('utf8')
            smeaning=sinner[wi].find('div',attrs={'class':'meaning'}).getText().encode('utf8')
            sexample=sinner[wi].find('div',attrs={'class':'example'}).getText().encode('utf8')
            udword=BeautifulSoup.BeautifulStoneSoup(sword, convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
            udmeaning=BeautifulSoup.BeautifulStoneSoup(smeaning, convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
            udexample=BeautifulSoup.BeautifulStoneSoup(sexample, convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
            res=[]
            res.append("\x0310,01[UD] \x02Word\x02:\x03 \x0307,01%s\x03" % udword)
            res.append("\x0310,01[UD] \x02Meaning\x02:\x03 \x0307,01%s\x03" % udmeaning)
            res.append("\x0310,01[UD] \x02Example\x02:\x03 \x0307,01%s\x03" % udexample)
           # display
            results['data']=res
        except Exception, err:
            results['error']=True
            results['data']="UD error: %s" % err
        finally:
            return results

    def moduleName(self):
        return "urbandictionary"

    def moduleDescription(self):
        return "returns an intellectually stimulating definition of the most important words and terms today!"

