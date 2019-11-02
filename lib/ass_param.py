#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os


class AssParam:

    def __init__(self):
        self.uid = os.getuid()
        self.etcDir = "/etc/partner"
        self.libDir = "/usr/lib/partner"
        self.pluginDir = os.path.join(self.libDir, "plugins")

        if os.getuid() == 0:
            self.tmpDir = "/tmp/partner"
            self.runDir = "/run/partner"
        else:
            self.tmpDir = "/tmp/user-%d-partner" % (os.getuid())            # fixme
            self.runDir = "/run/user/%d/partner" % (os.getuid())

        self.cfgFile = os.path.join(self.etcDir, "config.ini")
        self.pidFile = os.path.join(self.runDir, "partner.pid")

        self.mainloop = None
        self.dbusMainObject = None

        self.cfgObj = None
        self.envObj = None
        self.pluginManager = None
        self.reflexManager = None
