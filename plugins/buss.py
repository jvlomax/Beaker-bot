#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import json

import requests

from baseclass import Plugin


class Buss(Plugin):
    def __init__(self, skype):
        super(Buss, self).__init__(skype)
        self.command = "buss"
        self.stops = {
            'utsikten': ['761077514'], 'stakkevollan': ['761077543'], 'varden': ['761077684'],
            'uit': ['761077649'],
            'wito': ['761077674'],
            'jekta': ['761077476'], 'giæverbukta': ['761077661'],
            'flyplassen': ['761077638'], 'langnes': ['761077638'], 'fauske': ['760014408']
        }

    def getStopId(self, stop):
        r = requests.get(
            'http://hafas.utvikling01.reiseinfo.no/bin/dev/nri/rest.exe/v1.1/vs_restapi/location?authKey=cha-o2f-7s4-j3y&input=' + stop + '&format=json')
        data = json.loads(r.text)
        stop = data['LocationList']['StopLocation'][0]
        return [stop['id']], stop['name']

    def getTimes(self, startID, stopID, clock, list):
        """
        Put all possible trips into a list
        format:
        start-time, list of legs
        elements in list:
        (origin, time, buss nr, dest)
        """
        r = requests.get("http://hafas.utvikling01.reiseinfo.no/bin/dev/nri/rest.exe/v1.1/vs_restapi/trip?authKey=cha-o2f-7s4-j3y&time={}&originId={}&destId={}".format(str(clock), startID[0], stopID))
        root = ET.fromstring((r.text).encode('utf-8'))
        legList = root.iter('LegList')
        for legs in legList:
            trip = []
            origTime = legs[0][0].attrib['date']+" "+legs[0][0].attrib['time']
            date1 = datetime.strptime(origTime, '%Y-%m-%d %H:%M')
            now = datetime.now()
            if (now - date1) < timedelta(hours=23):
                for leg in legs:
                    try:
                        bussnr = leg.attrib['local']
                    except:
                        bussnr = leg.attrib['type']
                    start = leg[0].attrib['name']
                    time = leg[0].attrib['time']
                    stop = leg[1].attrib['name']
                    trip.append((bussnr, start, time, stop))
                list.append((origTime, trip))

    def message_received(self, args, status, msg):
        if len(args) < 2:
            start = str('utsikten')
            stop = str(args[0].decode('utf-8'))
        else:
            start = str(args[0].decode('utf-8'))
            stop = str(args[1].decode('utf-8'))

        if start.lower() in self.stops:
            startID = self.stops[start.lower()]
        else:
            startID, start = self.getStopId(start.lower())

        if stop.lower() in self.stops:
            stopID = self.stops[stop.lower()]
        else:
            stopID, stop = self.getStopId(stop.lower())

        clock = datetime.now().strftime('%H:%M')
        msg.Chat.SendMessage("Finding buss between {} and {} at {}".format(start, stop, str(clock)))

        list_of_trips = []
        for i in range(len(stopID)):
            self.getTimes(startID, stopID[i], clock, list_of_trips)
        list_of_trips.sort(key=lambda tup: tup[0])

        if len(list_of_trips) != 0 and len(list_of_trips) < 7:
            msg.Chat.SendMessage("Busses found ")
            num = len(list_of_trips)
            if num > 3:
                num = 3
            for i in range(num):
                elem = list_of_trips[i]
                msgTrip = ""
                trips = elem[1]
                for trip in trips:
                    msgTrip += "*{}* from {} to {} at {}\n".format(str(trip[0]), str(trip[1].encode('utf-8')), str(
                        trip[3].encode('utf-8')), str(trip[2]))
                msg.Chat.SendMessage(msgTrip)
        elif len(list_of_trips > 7):
            msg.Chat.SendMessage("Too many hops to display")
        else:
            msg.Chat.SendMessage("No busses found")

    def help(self, msg):
        msg.Chat.SendMessage(
            "Usage: @buss <start> stop\nWill tell you buss shcedule between two stops, start is optional, if no start then utsikten is assumed")
