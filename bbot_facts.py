from bbot_feature import BBOT_FEATURE
import urllib2
import BeautifulSoup

FACTS='http://randomfunfacts.com'

class BBOT_FACTS(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
        # commands
        self.myCommands=[]
        self.myCommands.append("!fact")

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        try:
            fdata='<td bordercolor="#FFFFFF"><font face="Verdana" size="4"><strong><i>'
            data=urllib2.urlopen(urllib2.Request(FACTS,headers={ "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24" })).read()
            fact=data[data.find(fdata)+len(fdata):data.find('</i>')]
            # display
            results['data']="\x0310,01[fact]\x03 \x0309,01%s\x03" % fact
        except:
            results['error']=True
            results['data']="fact lookup error"
        finally:
            return results

    def moduleName(self):
        return "fact"

    def moduleDescription(self):
        return "returns a random fact filled with useful info to help better your life!"

