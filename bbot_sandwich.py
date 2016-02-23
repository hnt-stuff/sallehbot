from bbot_feature import BBOT_FEATURE
import random

class BBOT_SANDWICH(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
	# seed
	random.seed(None)
        # commands
        self.myCommands=[]
        self.myCommands.append("!sandwich")
        # sammich
        self.food=[]
        self.food.append("\x0309boogars\0x03")
        self.food.append("\x0309used lingerie\0x03")
        self.food.append("\x0309rotten eggs\0x03")
        self.food.append("\x0309green eggs and ham\0x03")
        self.food.append("\x0309unicorn tears\0x03")
        self.food.append("\x0309turds\0x03")
        self.food.append("\x0309dead hooker juice\0x03")

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        try:
            ri=random.randint(0,len(self.food)-1)
            food=self.food[ri]
            result="sally makes %s a nice delicous sandwich made out of %s <3" % (nick,food)
            # display
            results['data']=result
        except Exception, err:
            results['error']=True
            results['data']="sammich error: %s" % err
        finally:
            return results

    def moduleName(self):
        return "sandwich"

    def moduleDescription(self):
        return "if you ask nicely salleh will make you a nice delicious sammich!"

