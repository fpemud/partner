#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import pwd
import glob
import logging


class AssReflexManager:

    def __init__(self, param):
        self.param = param
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        # reflex directories
        if self.param.uid == 0:
            self.reflexDirList = [
                os.path.join(self.param.etcDir, "reflex.d"),
                os.path.join(self.param.libDir, "reflex.d"),
            ]
        else:
            self.reflexDirList = [
                os.path.expanduser("~/.config/partner/reflex.d"),
            ]

        # reflex
        self.reflexDict = dict()                # dict<reflex-name, (reflex-property-dict, object_producer)>
        self._load_all_reflexes()

        # reflex object (aka reflex instance)
        self.reflexObjDict = dict()             # dict<reflex-fullname, reflex-object>
        self.on_reflex_environment_changed()

    def dispose(self):
        for fullname, obj in self.reflexObjDict.items():
            name = _reflex_split_fullname(fullname)[0]
            self._fini_flex_object(fullname, self.reflexDict[name][0], obj)

    def on_reflex_environment_changed(self):
        # get fullnames
        fullnameSet = set()
        for name in self.reflexDict:
            myFullnameSet = None

            propDict = self.reflexDict[name][0]
            if self.param.uid != 0:
                if propDict.get("need-user-login", False) and not self.param.envObj.is_user_login:
                    continue

            bDeny = False
            for pname in propDict.get("need-plugin", []):
                pobj = self.param.pluginManager.get_plugin_object(pname)
                ret = pobj.get_good_reflexes(name, self.reflexDict[name][0])
                if len(ret) == 0:
                    bDeny = True
                    break
                elif ret[0] == name:
                    continue
                else:
                    if myFullnameSet is None:
                        myFullnameSet = set(ret)
                    else:
                        myFullnameSet = set(ret) - myFullnameSet
            if bDeny:
                continue

            if myFullnameSet is None:
                fullnameSet |= {name}
            else:
                fullnameSet |= myFullnameSet

        # remove
        for fullname, obj in list(self.reflexObjDict.items()):
            if fullname in fullnameSet:
                continue
            name = _reflex_split_fullname(fullname)[0]
            self._fini_flex_object(fullname, self.reflexDict[name][0], obj)
            del self.reflexObjDict[fullname]

        # add
        for fullname in fullnameSet:
            if fullname in self.reflexObjDict:
                continue
            name = _reflex_split_fullname(fullname)[0]
            obj = self.reflexDict[name][1](fullname)
            self._init_flex_object(fullname, self.reflexDict[name][0], obj)
            self.reflexObjDict[fullname] = obj

    def _load_all_reflexes(self):
        for dn in self.reflexDirList:
            for fn in glob.glob(os.path.join(dn, "*")):
                bn = os.path.basename(fn)
                if bn.endswith(".rule"):
                    self._load_reflex_rule(fn)
                elif bn.endswith(".py"):
                    bn = bn[:-3]
                    self._load_reflex_script(dn, bn)
                elif os.path.isdir(fn) and os.path.exists(os.path.join(fn, "__init__.py")):
                    self._load_reflex_script(dn, bn)

    def _load_reflex_rule(self, filename):
        assert False

    def _load_reflex_script(self, dirname, pymodule):
        try:
            sys.path.append(dirname)
            exec("from %s import get_reflex_list" % (pymodule))
            exec("from %s import get_reflex_properties" % (pymodule))
            exec("from %s import get_reflex_object" % (pymodule))
            for name in eval("get_reflex_list()"):
                propDict = eval("get_reflex_properties(name)")
                producer = eval("get_reflex_object")

                set1 = set(propDict.get("need-plugin", []))
                set2 = set(self.param.pluginManager.get_plugin_name_list())
                ret = list(set1 - set2)
                if len(ret) > 0:
                    self.logger.warn("Reflex %s is not loaded because plugin %s does not exists." % (name, ret[0]))
                    continue

                self.reflexDict[name] = (propDict, producer)
        finally:
            sys.path.remove(dirname)

    def _init_flex_object(self, fullname, propDict, obj):
        obj.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__ + "." + fullname)
        obj.tmpdir = self.param.tmpDir      # fixme
        obj.my_name, obj.my_instance_name = _reflex_split_fullname(fullname)
        obj.my_fullname = fullname
        if self.param.uid != 0:
            obj.username = pwd.getpwuid(self.param.uid)[0]

        for pname in propDict.get("need-plugin", []):
            pobj = self.param.pluginManager.get_plugin_object(pname)
            pobj.reflex_pre_init(fullname, propDict, obj)

        obj.on_init()
        self.logger.info("Reflex \"%s\" initialized." % (fullname))

    def _fini_flex_object(self, fullname, propDict, obj):
        obj.on_fini()
        for pname in reversed(propDict.get("need-plugin", [])):
            pobj = self.param.pluginManager.get_plugin_object(pname)
            pobj.reflex_post_fini(fullname, propDict)
        self.logger.info("Reflex \"%s\" destroyed." % (fullname))


def _reflex_make_fullname(name, instance_name):
    if instance_name == "":
        return name
    else:
        return name + "." + instance_name


def _reflex_split_fullname(fullname):
    tlist = fullname.split(".")
    if len(tlist) == 1:
        return (fullname, "")
    else:
        assert len(tlist) == 2
        return (tlist[0], tlist[1])


class _ReflexRuleObject:

    def __init__(self, rule_file):
        pass
