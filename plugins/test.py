from baseclass import Plugin


class Test(Plugin):
    def __init__(self, skype):
        super(Test, self).__init__(skype)
        self.command = "test"

    def message_received(self, args, status, msg):
        msg.Chat.SendMessage("Nobody expects the norwegian inquisition")


if __name__ == "__main__":
    t = Test("Skype")
