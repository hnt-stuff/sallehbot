import time

SEND_DELAY=2
SEND_THRESH=3

class BBOT_FEATURE:
    def __init__(self,sendchat):
        self.sendchat=sendchat

    def registerDonna(self):
        pass

    def getCommands(self):
        return self.myCommands

    def getHandler(self):
        return self.processCommands

    def moduleName(self):
        pass
    
    def moduleDescription(self):
        pass

    def log(self,logdata):
	with open("%s.log" % self.moduleName(),"a") as lf:
	    lf.write("-[bbot donna submodule] * %s\n" % logdata)
	    lf.flush()

    def processCommands(self,nick,command,channel):
        data=self.handler(nick,command,channel)
        if data['error']:
	    self.log("feature error occured: %s" % data['data'])
            self.sendchat(channel,"[module] %s [error] %s" % (self.moduleName(),data['data']))
        else:
            # handle lines of data
	    if data['data']==None:
		pass
            elif type(data['data']) is str:
                self.sendchat(channel,data['data'])
            elif type(data['data']) is list:
                c=0
                for datares in data['data']:
                    self.sendchat(channel,datares)
                    c=c+1
                    if c>=SEND_THRESH:
                        time.sleep(SEND_DELAY)
                        c=0
