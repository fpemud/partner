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
        self.reflexDict = dict()                # dict<reflex-name, (context,modObj)>
        self._load_all_reflexes()

        # reflex initialize and start
        for reflexName, value in self.reflexDict.items():
            context, modObj = value
            modObj.init(context)
            self.param.mainloop.call_soon(self._run_reflex(context, modObj))

    def dispose(self):
        # reflex finalization
        for reflexName, value in self.reflexDict.items():
            context, modObj = value
            modObj.fini(context)

    def _load_all_reflexes(self):
        for dn in self.reflexDirList:
            for fn in glob.glob(os.path.join(dn, "*")):
                if fn.endswith(".py"):
                    self.__load_reflex_python_script(fn)
                else:
                    # FIXME we should support other script in future
                    pass

    def __load_reflex_python_script(self, fullfn):
        context = _ReflexContext()
        modName, modObj = AssUtil.loadPythonFile(fullfn)
        self.reflexDict[fullfn] = (context, modObj)
        self.logger.info("Reflex (python script %s) loaded." % (fullfn))

    async def _run_reflex(self, context, modObj):
        while True:
            brainNode, responseFunc, privateData = await modObj.stimulus(context)
            # FIXME: decide not do response
            if responseFunc.__dict__["partner.reflex.response"]:
                await responseFunc(context, privateData)
            elif responseFunc.__dict__["partner.reflex.parallel_response"]:
                self.param.mainloop.call_soon(responseFunc(context, privateData))
            else:
                assert False


class _ReflexContext:

    def __init__(self):
        self.logger = None
        self.tmpdir = None
