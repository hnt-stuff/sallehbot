from bbot_feature import BBOT_FEATURE
import urllib2
import BeautifulSoup

IPURL='http://geoiptool.com/en/?IP='

class BBOT_GEOLOCATION(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
        # commands
        self.myCommands=[]
        self.myCommands.append("!ip")

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        if len(data)<2:
            self.log("missing param")
            return results
        target=data[1]
        try:
            # log
            self.log("looking up %s" % target)
            # lookup
            ipdata=urllib2.urlopen(urllib2.Request(IPURL+target,headers={ "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24" })).read()
            hostname=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'Host Name:')).getText().encode('utf8')
            ipaddy=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'IP Address:')).getText().encode('utf8')
            country=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'Country:')).getText().encode('utf8')
            countrycode=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'Country code:')).getText().encode('utf8')
            region=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'Region:')).getText().encode('utf8')
            city=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'City:')).getText().encode('utf8')
            postalcode=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'Postal code:')).getText().encode('utf8')
            callingcode=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'Calling code:')).getText().encode('utf8')
            loc_long=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'Longitude:')).getText().encode('utf8')
            loc_lat=BeautifulSoup.BeautifulSoup(self.extractBody(ipdata,'Latitude:')).getText().encode('utf8')
            # check data
            if hostname.strip()=='' and country.strip()=='' and region.strip()=='':
                self.log("ip/host lookup empty")
                results['data']="[Geolocation] not found"
                return results
            # prep
            chatdata="\x0303,01[IP Address]:\x03 \x0315,01%s\x03 - \x0303,01[Hostname]:\x03 \x0315,01%s\x03 - \x0303,01[Country]:\x03 \x0315,01%s\x03 - \x0303,01[Country Code]:\x03 \x0315,01%s\x03 - \x0303,01[Region]:\x03 \x0315,01%s\x03 - \x0303,01[City]:\x03 \x0315,01%s\x03 - \x0303,01[Postal Code]:\x03 \x0315,01%s\x03 - \x0303,01[Calling Code]:\x03 \x0315,01%s\x03 - \x0303,01[Longitude]:\x03 \x0315,01%s\x03 - \x0303,01[Latitude]:\x03 \x0315,01%s\x03" % (ipaddy,hostname,country,countrycode,region,city,postalcode,callingcode,loc_long,loc_lat)
            # display
            results['data']=chatdata
        except Exception, err:
            results['error']=True
            results['data']="geo error: %s" % err
        finally:
            return results

    def moduleName(self):
        return "geolocate"

    def moduleDescription(self):
        return "given an ip or host will return various geolocation and lookup information"

    def extractBody(self,data,target):
        # find target, then find BEGIN TAG after, then END TAG after begin tag and return that.
        endTag='</td>'
        i=data.find(target)
        j=data[i+len(target):].find(endTag)
        j2=data[i+len(target)+j+len(endTag):].find(endTag)
        return data[i+len(target)+j+len(endTag):i+len(target)+j+len(endTag)+j2]

