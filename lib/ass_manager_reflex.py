#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import glob
import logging
from ass_util import AssUtil
from ass_param import AssConst


class AssReflexManager:

    def __init__(self, param):
        self.param = param
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        # reflex directories
        if os.getuid() == 0:
            self.reflexDirList = [
                os.path.expanduser("~/.config/partner/reflex.d"),
                os.path.join(AssConst.libDir, "reflex.d"),
            ]
        else:
            self.reflexDirList = [
                os.path.expanduser("~/.config/partner/reflex.d"),
            ]

        # reflex
        self.reflexDict = dict()                # dict<reflex-name, [context,initFunc,finiFunc,stimulusFunc]>
        self._load_all_reflexes()

    def dispose(self):
        for pymodule, obj in self.reflexObjDict.items():
            assert False

    def _load_all_reflexes(self):
        for dn in self.reflexDirList:
            for fn in glob.glob(os.path.join(dn, "*")):
                if fn.endswith(".py"):
                    self._load_reflex_python_script(dn)
                else:
                    # FIXME we should support other script in future
                    pass

    def _load_reflex_python_script(self, fullfn):
        context = _ReflexContext()
        modName, modObj = AssUtil.loadPythonFile(fullfn)
        self.reflexDict[fullfn] = [context, modObj]


class _ReflexContext:

    def __init__(self):
        self.logger = None
        self.tmpdir = None
