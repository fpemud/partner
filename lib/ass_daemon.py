#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import pwd
import dbus
import signal
import shutil
import logging
import configparser
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
from ass_util import AssUtil
from ass_param import AssConst
from ass_common import AssReflexEnvironment
from ass_manager_plugin import AssPluginManager
from ass_manager_reflex import AssReflexManager


class AssDaemon:

    def __init__(self, param):
        self.param = param

    def run(self):
        try:
            AssUtil.mkDirAndClear(AssConst.tmpDir)
            AssUtil.mkDirAndClear(AssConst.runDir)

            logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
            logging.getLogger().setLevel(AssUtil.getLoggingLevel(self.param.logLevel))

            # load configuration
            self._load_config()

            # write pid file
            with open(AssConst.pidFile, "w") as f:
                f.write(str(os.getpid()))

            # create main loop
            DBusGMainLoop(set_as_default=True)
            self.param.mainloop = GLib.MainLoop()

            # start DBUS API server
            # if os.getuid() == 0:
            #     self.param.dbusMainObject = DbusObjectSystem(self.param)
            # else:
            #     self.param.dbusMainObject = DbusObjectSession(self.param)

            # reflex environment
            self.param.envObj = AssReflexEnvironment(self.param)
            if AssConst.uid != 0:
                self.userNewHandle = dbus.SystemBus().add_signal_receiver(self._dbus_signal_user_new, dbus_interface="org.freedesktop.login1.Manager", signal_name="UserNew")
                self.userRemoveHandle = dbus.SystemBus().add_signal_receiver(self._dbus_signal_user_new, dbus_interface="org.freedesktop.login1.Manager", signal_name="UserRemoved")

            # business object
            self.param.pluginManager = AssPluginManager(self.param)
            self.param.reflexManager = AssReflexManager(self.param)

            # start main loop
            logging.info("Mainloop begins.")
            GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGINT, self._sigHandlerINT, None)
            GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGTERM, self._sigHandlerTERM, None)
            self.param.mainloop.run()
            logging.info("Mainloop exits.")
        finally:
            if self.param.reflexManager is not None:
                self.param.reflexManager.dispose()
                self.param.reflexManager = None
            if self.param.pluginManager is not None:
                self.param.pluginManager.dispose()
                self.param.pluginManager = None
            if hasattr(self, "userRemoveHandle"):
                dbus.SystemBus().remove_signal_receiver(self.userRemoveHandle)
            if hasattr(self, "userNewHandle"):
                dbus.SystemBus().remove_signal_receiver(self.userNewHandle)
            logging.shutdown()
            shutil.rmtree(AssConst.runDir)
            shutil.rmtree(AssConst.tmpDir)

    def _sigHandlerINT(self, signum):
        logging.info("SIGINT received.")
        self.param.mainloop.quit()
        return True

    def _sigHandlerTERM(self, signum):
        logging.info("SIGTERM received.")
        self.param.mainloop.quit()
        return True

    def _load_config(self):
        self.cfgObj = dict()
        if os.path.exists(AssConst.cfgFile):
            cfg = configparser.SafeConfigParser()
            cfg.read(AssConst.cfgFile)
            for section in cfg.sections():
                self.cfgObj[section] = dict()
                for option in cfg.options(section):
                    self.cfgObj[section][option] = AssUtil.stripComment(cfg.get(section, option))

    def _dbus_signal_user_new(self, uid, object_path):
        if uid != AssConst.uid:
            return
        assert not self.param.envObj.is_user_login
        self.param.envObj.is_user_login = True
        logging.info("User %s appears." % (pwd.getpwuid(AssConst.uid)[0]))
        self.param.envObj.changed()

    def _dbus_signal_user_remove(self, uid, object_path):
        if uid != AssConst.uid:
            return
        assert self.param.envObj.is_user_login
        self.param.envObj.is_user_login = False
        logging.info("User %s disappears." % (pwd.getpwuid(AssConst.uid)[0]))
        self.param.envObj.changed()
