__author__ = 'george'
from baseclass import Plugin
import time
from apscheduler.scheduler import Scheduler

class AreWeDone(Plugin):
    def __init__(self, skype):
        super(AreWeDone, self).__init__(skype)
        self.command = "arewedoneyet"
        self.sched = Scheduler()
        self.sched.start()
        self.sched.add_cron_job(self.set_topic, hour="*", minute=2, day_of_week="monun")
    def message_received(self, args, status, msg):
        cur_time = time.localtime()
        if cur_time.tm_mday == 31 or cur_time.tm_mday == 1:
            time_left = 1 - cur_time.tm_mday % 31
            hours_left = 23 - cur_time.tm_hour
            mins_left = 59 - cur_time.tm_min
            msg.Chat.SendMessage("%d days, %d hours and %d mins left until we are done" % (time_left, hours_left, mins_left))
            print "%d days, %d hours and %d mins left until we are done" % (time_left, hours_left, mins_left)
        else:
            msg.Chat.SendMessage("You are now done. Please visit http://www.nav.no for more information")


    def set_topic(self):
        channel = "#stigrk85/$jvlomax;b43a0c90a2592b9b"
        chat = self.skype.Chat(channel)
        cur_time = time.localtime()
        days_left = 1 - cur_time.tm_mday % 31
        time_left = 24 - cur_time.tm_hour + days_left * 24
        if cur_time.tm_hour >= 21 or cur_time.tm_hour < 6:
            tod = "night"
        else:
            tod= "day"
        if days_left > 0:
            left = "second"
        else:
            left = "final"
        if cur_time.tm_mday == 1:
            chat.SendMessage("/topic {} of the {} day - {} hours remain".format(tod, left, time_left))
        else:
            chat.SendMessage("Congratulations, You have survived. Please visit http://www.nav.no for more information".format(tod, left, time_left))



    
    
