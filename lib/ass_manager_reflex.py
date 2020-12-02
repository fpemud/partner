#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import glob
import logging
from ass_param import AssConst


class AssReflexManager:

    def __init__(self, param):
        self.param = param
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        # reflex directories
        if AssConst.uid == 0:
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
                bn = os.path.basename(fn)
                if bn.endswith(".py"):
                    bn = bn[:-3]
                    self._load_reflex_python_script(dn, bn)
                else:
                    # FIXME we should support other script in future
                    pass

    def _load_reflex_python_script(self, dirname, pymodule):
        try:
            sys.path.append(dirname)
            context = _ReflexContext()
            initFunc = None
            finiFunc = None
            stimulusFunc = None
            exec("from %s import init as initFunc" % (pymodule))
            exec("from %s import fini as finiFunc" % (pymodule))
            exec("from %s import stimulus as stimulusFunc" % (pymodule))
            self.reflexDict[pymodule] = [context, initFunc, finiFunc, stimulusFunc]
        finally:
            sys.path.remove(dirname)


class _ReflexContext:

    def __init__(self):
        self.logger = None
        self.tmpdir = None
