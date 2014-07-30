__author__ = 'george'
import httplib
from baseclass import Plugin
from apscheduler.scheduler import Scheduler
import wikipedia as wiki
import requests
import urllib

class Wikipedia(Plugin):
    def __init__(self, skype):
        super(Wikipedia, self).__init__(skype)
        self.daily_channels = ["#stigrk85/$jvlomax;b43a0c90a2592b9b"]
        self.sched = Scheduler()
        self.sched.start()
        self.plugin_name = "wikipedia"
        self.sched.add_cron_job(self.dailyWikipedia, hour=18, minute=0, day_of_week="mon-sun")

    def message_received(self, msg, status):
        text = msg.Body
        if text[0] == "@":
            text = text[1:]
            try:
                command = text.split(" ")[0]
            except:
                print("exception in wikipedia")
                command = text
            if command.lower() == "wikipedia":
                terms = text.split(" ")[1:]
                print(terms)
                if (len(terms) == 1 and terms[0] == "random") or not terms:
                    url = self.fetch_randWiki()
                    msg.Chat.SendMessage(url)
                else:
                    try:
                        page = wiki.wikipedia.page(" ".join(terms))
                        if page.url:
                            msg.Chat.SendMessage(urllib.unquote(page.url))
                        else:
                            msg.Chat.SendMessage("Could not find any results for {}".format(" ".join(terms)))
                    except wiki.exceptions.DisambiguationError:
                        msg.Chat.SendMessage("Your search is disambigous")
                    except wiki.exceptions.PageError:
                         msg.Chat.SendMessage("Could not find any results for {}".format(" ".join(terms)))       

    def fetch_randWiki(self):
        r = requests.get("http://en.wikipedia.org/wiki/Special:Random")
        return r.url

    def dailyWikipedia(self):
        for channel in self.daily_channels:
            chat = self.skype.Chat(channel)
            chat.SendMessage("Dagens random wikipedia: " + self.fetch_randWiki())


        
   
    