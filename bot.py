from __future__ import print_function, unicode_literals

import time
import os, sys
import Skype4Py
import ConfigParser
import atexit
import shlex

class SkypeBot(object):
    def __init__(self):
        self.name = "Default name"
        self.tag = None
        #self.skype = Skype4Py.Skype(Events=self, Transport="dbus")
        self.skype = Skype4Py.Skype(Events=self)

        self.plugin_classlist = []
        self.enabled_plugins = []
        self.disabled_plugins = []

        self.load_settings()
        self.load_plugins()
        plugin_names = [type(x).__name__ for x in self.plugin_classlist]
        print("loaded plugins\n Active plugins: {}".format(" ".join(plugin_names)))
        if not self.skype.Client.IsRunning:
            print("skype not running, starting skype")
            self.skype.Client.Start()
            time.sleep(30)
            print("skype is now running")
        self.skype.FriendlyName = "Beaker"
        self.skype._SetTimeout = 20
        self.skype.Attach()
        if not self.tag:
            self.tag = "@"
        print("I'm ready")
        self.skype.ChangeUserStatus(Skype4Py.cusOnline)
        atexit.register(self.on_exit)
        self.enabled_plugins = self.plugin_classlist

    def MessageStatus(self, msg, status):
        print("received message: {}".format(msg.Body))
        if status == Skype4Py.cmsReceived and msg.Body[0] == self.tag:
            command = msg.Body.split(" ")[0][1:].lower()
            
            args = shlex.split(msg.Body.encode("utf-8"))[1:]
            for c in self.enabled_plugins:
                if c.command == command or not c.uses_command:
                    c.message_received(args, status, msg)
                    if c.uses_command:
                        return

            #internal handling for bot spesific commands



            if command.lower() == "help":
                if not args:
                    msg.Chat.SendMessage("This is beaker bot help. For a list of avilable commands, type {}help commands".format(self.tag))
                if args[0].lower() == "commands":
                    commands = ["{}{}".format(self.tag, x.command) for x in self.plugin_classlist if x.uses_command]
                    msg.Chat.SendMessage("available commands: {}".format(", ".join(commands)))
                    return
                else:
                    for plugin in self.enabled_plugins:
                        if plugin == args[0]:
                            plugin.help(msg)
            elif command.lower() == "plugins":
                self.pluginHandler(args, msg)



    def pluginHandler(self, args, msg):
       #TODO: PLease replace with some try catch, or something that doesn't make python look like it was smashed against a wall
        if args:
            if len(args) > 1:
                plugin = args[1]

                if args[0] == "enable":
                    print("enable")
                    if plugin in [c.command for c in self.enabled_plugins]:
                        msg.Chat.SendMessage("{} is already enabled".format(plugin))
                    else:
                        for module in self.disabled_plugins:
                            if module.command == plugin:
                                self.enabled_plugins.append(module)
                                self.disabled_plugins.remove(module)
                                msg.Chat.SendMessage("{} has now been enabled".format(plugin))
                                return

                elif args[0] == "disable":
                    print("disable")
                    if plugin in [c.command for c in self.disabled_plugins]:
                        msg.Chat.SendMessage("{} is already disabled".format(plugin))
                    else:
                        for module in self.enabled_plugins:
                            if module.command == plugin:
                                self.disabled_plugins.append(module)
                                self.enabled_plugins.remove(module)
                                msg.Chat.SendMessage("{} has now been disabled".format(plugin))
                                return
                
                else:
                    print("Uknown arg {}".format(args[0]))
                    msg.Chat.Send("Usage: @plugin <disable|enable> <plugin name>")
            elif args[0] == "reload":
                self.plugin_classlist = []
                self.load_plugins()

                self.enabled_plugins = []
                old_disabled_plugins = self.disabled_plugins
                self.disabled_plugins = []
                for p in self.plugin_classlist:
                    print("looking at plugin {}".format(p))
                    if p in old_disabled_plugins:
                        self.disabled_plugins.append(p)
                    else:
                        self.enabled_plugins.append(p)
                print("Enabled plugins: {}".format(self.enabled_plugins))
                print("Disabled Plugins: {}".format(self.disabled_plugins))
            else:
                msg.Chat.SendMessage("Usage: @plugin <disable|enable> <plugin name>")
        else:
            msg.Chat.SendMessage("Enabled plugins:")
            plugins = [c.command for c in self.enabled_plugins]
            msg.Chat.SendMessage("{}".format(", ".join(plugins)))

    def load_plugins(self):
        # print("loading plugins")
        sys.path.append("plugins")
        from baseclass import Plugin
        for root, dirs, files in os.walk("plugins"):
            candidates = [fname for fname in files if fname.endswith(".py") and not fname.startswith(("__"))]
            for c in candidates:
                if c == "baseclass.py": #hacky way to eliminate the plugin base class
                    continue
                modname = os.path.splitext(c)[0]
                module = __import__(modname)
                for cls in dir(module):
                    tmp = getattr(module, cls)
                    try:
                        if issubclass(tmp, Plugin):
                            instance = tmp(self.skype)
                            self.plugin_classlist.append(instance)
                    except:
                        pass #This is not the class you are looking for

    def load_settings(self):
        print("loading settings")
        config = ConfigParser.RawConfigParser()
        config.read("settings.conf")
        self.name = config.get("general", "name")
        self.tag = str(config.get("general", "tag"))
        plugins = config.options("plugins")
        for plugin in plugins:
            if config.getboolean("plugins", plugin):
                self.enabled_plugins.append(plugin)

    def on_exit(self):
        self.skype.ChangeUserStatus(Skype4Py.cusDoNotDisturb)

if __name__ == "__main__":
    bot = SkypeBot()
    while True:
        pass        
       

