__author__ = 'george'
import httplib
from baseclass import Plugin
from apscheduler.scheduler import Scheduler




class NSFW(Plugin):
    def __init__(self, skype):
        super(NSFW, self).__init__(skype)
        self.daily_channels = ["#stigrk85/$jvlomax;b43a0c90a2592b9b"]
        self.sched = Scheduler()
        self.sched.start()
        self.command = "nsfw"
        self.sched.add_cron_job(self.dailyNSFW, hour=19, minute=0, day_of_week="mon-sun")

    def message_received(self, args, status, msg):
        url = self.fetch_randNSFW()
        msg.Chat.SendMessage(url)


    def fetch_randNSFW(self):
        conn = httplib.HTTPConnection("www.reddit.com")
        conn.request("GET", "/r/randnsfw")
        redirect = conn.getresponse().getheader("Location")
        return redirect

    def dailyNSFW(self):
        for channel in self.daily_channels:
            chat = self.skype.Chat(channel)
            chat.SendMessage("Dagens /r/randnsfw: " + self.fetch_randNSFW())
