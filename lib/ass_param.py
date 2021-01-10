#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os


class AssConst:

    etcDir = "/etc/partner"
    libDir = "/usr/lib/partner"
    cfgFile = os.path.join(etcDir, "config.ini")


class AssParam:

    def __init__(self, userMode):
        self.mainloop = None
        self.dbusMainObject = None

        if not userMode:
            self.tmpDir = "/tmp/partner"
            self.runDir = "/run/partner"
        else:
            self.tmpDir = "/tmp/user-%d-partner" % (os.getuid())            # fixme
            self.runDir = "/run/user/%d/partner" % (os.getuid())
        self.pidFile = os.path.join(self.runDir, "partner.pid")

        self.cfgObj = None
        self.envObj = None
        self.reflexManager = None
