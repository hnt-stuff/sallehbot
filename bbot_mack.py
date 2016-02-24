from bbot_feature import BBOT_FEATURE
import random

class BBOT_MACK(BBOT_FEATURE):
    def __init__(self,sendchat):
        # super
        BBOT_FEATURE.__init__(self,sendchat)
	# seed
	random.seed(None)
        # commands
        self.myCommands=[]
        self.myCommands.append("!mack")
        # sammich
        self.oneliners=[]
        self.oneliners.append("\x0309***\x03 looks deeply into \x0313___\x03's eyes and says...hey baby..you must be sitting on the F5 key...cuz dat ASS is \x0309REFRESHING!!!!!\x03")
        self.oneliners.append("\x0309***\x03 walks up to \x0313___\x03 and says delicately into their earlobe...do you chafe when cuffed?")
        self.oneliners.append("\x0309***\x03 removes pants and walks up to \x0313___\x03 then looks straight into their eyes and asks....'so what are we gonna do about this?'")
        self.oneliners.append("\x0309***\x03 backs that ass up on \x0313___\x03")
        self.oneliners.append("\x0309***\x03 stares at \x0313___\x03 from a dark corner....eyes glistening in the darkness....some drool drips to the floor!")
        self.oneliners.append("\x0309***\x03 looks at \x0313___\x03 .....and feels a little... RAPEY!")
        self.oneliners.append("\x0309***\x03 attempts to finger \x0313___\x03 .....its super effective!!")
        self.oneliners.append("\x0309***\x03 shoves their hand straight down \x0313___\x03's pants!! Call the cops!")
        self.oneliners.append("\x0309***\x03 wants \x0313___\x03 to know that its not rape if your holding hands.")
        self.oneliners.append("\x0309***\x03 wants to hold \x0313___\x03 like a bowling ball!")

    def handler(self,nick,data,channel):
        results={}
        results.update(error=False,data=None)
        try:
			if len(data)<2:
				self.log('missing target of affection %i' % len(data))
				return results
			if data[1].strip()=='':
				self.log('missing target of affection %i' % len(data))
				return results
			target=data[1].strip()
			if nick==target:
				self.log('sending masturbatory mack')
				result='%s looks directly into every one of your eyes....then begins to furiously masturbate!!!!' % nick
			else:
				ri=random.randint(0,len(self.oneliners)-1)
				game=self.oneliners[ri]
				self.log('sending mack')
				result=game.replace('***',nick).replace('___',target)
			# display
			results['data']=result
        except Exception, err:
            results['error']=True
            results['data']="mack error: %s" % err
        finally:
            return results

    def moduleName(self):
        return "mack"

    def moduleDescription(self):
        return "if you want to get laid salleh will help! only param is the target of your affection. finally a way to kick some sweet sweet game!!"

