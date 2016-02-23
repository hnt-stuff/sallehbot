from bbot_feature import BBOT_FEATURE
import urllib2
import json

SEARCH="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="

class BBOT_GOOGLESEARCH(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
        # commands
        self.myCommands=[]
        self.myCommands.append("!google")

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        # check search term
        if len(data)<2:
            return results
        try:
            term=" ".join(data[1:])
            # log
            self.log("searching for %s" % term)
            searchresults=[]
            # search
            data=json.loads(urllib2.urlopen(urllib2.Request(SEARCH+term.replace(' ','%20'),headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24","Referer":"http://www.ninjas.com"})).read())
            nres=data['responseData']['cursor']['resultCount']
            tres=data['responseData']['cursor']['searchResultTime']
            for res in data['responseData']['results']:
                glink=res['url']
                gtitle=res['titleNoFormatting']
                # first result
                break
            # display gres
            searchresults.append("Link [ %s ] " % glink)
            searchresults.append("Title [ %s ] " % gtitle)
            searchresults.append("Total search results: %s" % nres)
            searchresults.append("Search time: %s" % tres)

            results['data']=searchresults
        except Exception, err:
            results['error']=True
            results['data']="google search error: %s" % err
        finally:
            return results

    def moduleName(self):
        return "googlesearch"

    def moduleDescription(self):
        return "uses google to search for your search term"

