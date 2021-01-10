#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import signal
import shutil
import logging
import asyncio
import asyncio_glib
import configparser
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
from ass_util import AssUtil
from ass_param import AssConst
from ass_manager_reflex import AssReflexManager


class AssDaemon:

    def __init__(self, param):
        self.param = param

    def run(self):
        try:
            AssUtil.prepareTransientDir(self.param.runDir, os.getuid(), os.getgid(), 0o755)
            AssUtil.prepareTransientDir(self.param.tmpDir, os.getuid(), os.getgid(), 0o755)

            logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
            logging.getLogger().setLevel(AssUtil.getLoggingLevel(self.param.logLevel))
            logging.info("Program begins.")

            # load configuration
            self._load_config()

            # write pid file
            AssUtil.writePidFile(self.param.pidFile)

            # create main loop
            DBusGMainLoop(set_as_default=True)
            asyncio.set_event_loop_policy(asyncio_glib.GLibEventLoopPolicy())
            self.param.mainloop = asyncio.get_event_loop()

            # start DBUS API server
            # if os.getuid() == 0:
            #     self.param.dbusMainObject = DbusObjectSystem(self.param)
            # else:
            #     self.param.dbusMainObject = DbusObjectSession(self.param)

            # business object
            self.param.reflexManager = AssReflexManager(self.param)

            # start main loop
            logging.info("Mainloop begins.")
            GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGINT, self._sigHandlerINT, None)
            GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGTERM, self._sigHandlerTERM, None)
            self.param.mainloop.run_forever()
            logging.info("Mainloop exits.")
        finally:
            if self.param.reflexManager is not None:
                self.param.reflexManager.dispose()
                self.param.reflexManager = None
            logging.shutdown()
            shutil.rmtree(self.param.runDir)
            shutil.rmtree(self.param.tmpDir)

    def _sigHandlerINT(self, signum):
        logging.info("SIGINT received.")
        self.param.reflexManager.cancelAll()
        self.param.mainloop.call_soon_threadsafe(self.param.mainloop.stop)
        return True

    def _sigHandlerTERM(self, signum):
        logging.info("SIGTERM received.")
        self.param.reflexManager.cancelAll()
        self.param.mainloop.call_soon_threadsafe(self.param.mainloop.stop)
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
