#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import dbus
import dbus.service


################################################################################
# DBus API (system bus)
################################################################################
#
# ==== Main Application ====
# Service               org.fpemud.Partner
# Interface             org.fpemud.Partner
# Object path           /
#
# Properties:
#   list<str>         ActionList
#
# Methods:
#   void              Ask(question:str)
#
# Signals:
#   Say(message:str)
#


################################################################################
# DBus API (session bus)
################################################################################
#
# ==== Main Application ====
# Service               org.fpemud.Partner
# Interface             org.fpemud.Partner
# Object path           /
#
# Properties:
#   list<str>         ActionList
#   int               IdleTimeout
#
# Methods:
#   void              Poke()
#   void              Ask(question:str)
#
# Signals:
#   Say(message:str)
#   Emote(emotion:str)
#   SayWithEmotion(message:str, emotion:str)
#
#
#


class AssServiceException(Exception):

    def __init__(self, msg):
        self.msg = msg


class DbusObjectSystem(dbus.service.Object):

    def __init__(self, param):
        self.param = param
        bus_name = dbus.service.BusName('org.fpemud.Partner', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/org/fpemud/VirtService')

    def release(self):
        self.remove_from_connection()

    @dbus.service.method('org.fpemud.Partner', sender_keyword='sender', in_signature='s', out_signature='s')
    def Ask(self, networkType, sender=None):
        #        uid = AssUtil.dbusGetUserId(self.connection, sender)
        return ""


class DbusObjectSession(dbus.service.Object):

    def __init__(self, param):
        self.param = param
        bus_name = dbus.service.BusName('org.fpemud.Partner', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/org/fpemud/VirtService')

    def release(self):
        self.remove_from_connection()

    @dbus.service.method('org.fpemud.Partner')
    def Poke(self):
        pass

    @dbus.service.signal('org.fpemud.Partner', signature='s')
    def Say(self, message):
        pass

    @dbus.service.signal('org.fpemud.Partner', signature='s')
    def Emote(self, emotion):
        pass

    @dbus.service.signal('org.fpemud.Partner', signature='ss')
    def SayWithEmotion(self, message, emotion):
        pass
