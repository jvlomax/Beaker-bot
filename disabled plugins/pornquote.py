from random import randrange
import re
import urllib
from baseclass import Plugin


class PornQuote(Plugin):
    def __init__(self, skype):
        super(PornQuote, self).__init__(skype)
        self.command = "pornquote"

    def message_received(self, args, status, msg):
        result = []
        while len(result) < 1:
            socket = urllib.urlopen("http://www.youporn.com/random/video/")
            htmlSource = socket.read()
            socket.close()
            result = re.findall('<p class="message">((?:.|\\n)*?)</p>', htmlSource)
        
        msg.Chat.SendMessage(result[randrange(len(result))])
        return
