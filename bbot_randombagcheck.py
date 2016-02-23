from bbot_feature import BBOT_FEATURE
import random

class BBOT_RANDOMBAGCHECK(BBOT_FEATURE):
    def __init__(self,sendchat,sendraw):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
	# seed
	random.seed(None)
        # commands
        self.myCommands=[]
        self.myCommands.append("!randombagcheck")
        # raw
        self.sendraw=sendraw
        # bagcheck messages
        self.reasons=[]
        self.reasons.append("*** had a knife in a back pocket during a patdown! The bouncer does not approve!")
        self.reasons.append("*** tried to bribe the bouncer at club HnT... the bouncer kicks you da fug out!")
        self.reasons.append("*** tried to kick it to one of ChunLo's underaged daughters... ChunLo: OHH u want to put your eggroll in my daughters soy sauce? I PUT MY EGGROLL IN YOUR BUNGHOLE!!")
	self.reasons.append("*** was followed home by a drone WITH LASERS!")
	self.reasons.append("*** suddenly grew a beard. *** now looks suspicious! TSA drop kicks *** the hell out!")
	self.reasons.append("*** was caught with a bag of herr0n up the bunghole!")
	self.reasons.append("Someone thought *** said bomb. TSA DROP KICKED ***s face off!!!")
        # nick (until fixed with config)
        self.nick="sally_"

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        # target
        if len(data)<2:
            self.log("missing target param")
            return results
        target=data[1]
        if target==self.nick:
            target=nick
        self.log("random bag check on %s" % target)
        try:
            ri=random.randint(0,len(self.reasons)-1)
            rmessage=self.reasons[ri].replace("***",target)
            self.sendraw("KICK %s %s :%s\n" % (channel,target,rmessage))
        except Exception, err:
            results['error']=True
            results['data']="randombagcheck error: %s" % err
        finally:
            return results

    def moduleName(self):
        return "randombagcheck"

    def moduleDescription(self):
        return "helpfully performs a random bag check on the specified user. remember if you see something, say something!"

