#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os


class AssConst:

    etcDir = "/etc/partner"
    libDir = "/usr/lib/partner"
    pluginDir = os.path.join(libDir, "plugins")
    if os.getuid() == 0:
        tmpDir = "/tmp/partner"
        runDir = "/run/partner"
    else:
        tmpDir = "/tmp/user-%d-partner" % (os.getuid())            # fixme
        runDir = "/run/user/%d/partner" % (os.getuid())

    cfgFile = os.path.join(etcDir, "config.ini")
    pidFile = os.path.join(runDir, "partner.pid")


class AssParam:

    def __init__(self):
        self.mainloop = None
        self.dbusMainObject = None

        self.cfgObj = None
        self.envObj = None
        self.reflexManager = None
