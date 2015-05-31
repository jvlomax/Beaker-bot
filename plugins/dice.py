from baseclass import Plugin
from random import randint

class Dice(Plugin):
    def __init__(self, skype):
        super(Dice, self).__init__(skype, "roll")
        self.command = "roll"

    def message_received(self, args, status, msg):
        num_dice, eyes = args[0].split("d")
        total = 0
        for x in range(0, int(num_dice)):
            total += randint(1, int(eyes))

        msg.Chat.SendMessage(str(total))
