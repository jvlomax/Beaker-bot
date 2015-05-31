__author__ = 'george'
from baseclass import Plugin
import urllib
from random import choice
from apscheduler.scheduler import Scheduler

class IsItWar(Plugin):
    def __init__(self, skype):
        super(IsItWar, self).__init__(skype)
        self.falseMessages =["The world is still safe, Russia has not declared war yet", "http://suptg.thisisnotatrueending.com/archive/29138254/images/1388285593271.jpg", "http://www.meh.ro/original/2010_03/meh.ro3771.jpg", "http://d24w6bsrhbeh9d.cloudfront.net/photo/arpBmWp_700b_v1.jpg", "http://d24w6bsrhbeh9d.cloudfront.net/photo/aXb2VAv_700b.jpg", "http://d24w6bsrhbeh9d.cloudfront.net/photo/aLKXd6v_700b.jpg", "http://img-9gag-lol.9cache.com/photo/aGVZmd7_460sa_v1.gif"]
        self.sched = Scheduler()
        self.sched.start()
        self.sched.add_interval_job(self.is_it_war, minutes=10)
        self.command = "isitwaryet"

    def message_received(self, args, status, msg):

        res = urllib.urlopen("http://www.bbc.co.uk/news")
        text = res.read()
        if "declares war" in text.lower():
            msg.Chat.SendMessage("Brace your selves, mother Russia is coming")
        else:
            msg.Chat.SendMessage(choice(self.falseMessages))

    def is_it_war(self):
        print "checking if war"
        res = urllib.urlopen("http://www.bbc.co.uk")
        text = res.read()
        if "declares war" in text.lower():
            chat = self.skype.Chat("#stigrk85/$jvlomax;b43a0c90a2592b9b")
            chat.SendMessage("Brace yourself, Mother Russia is coming")
        


    def help(self, msg):
        msg.Chat.SendMessage("usage: @isitwaryet\nWill tell you if Russia has declared war")
