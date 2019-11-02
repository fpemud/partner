#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import glob
import logging
import toposort


class AssPluginManager:

    def __init__(self, param):
        self.param = param
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self.pluginDir = os.path.join(self.param.libDir, "plugins.d")

        # load and initialized all plugins
        self.pluginDict = dict()        # dict<plugin-name, (plugin-property-dict, plugin-object)>
        self._load_all_plugins()
        self._init_all_plugins()

    def dispose(self):
        for name in reversed(self._get_sorted_plugin_names()):
            self.pluginDict[name][1].dispose()
            self.param.envObj.remove_plugin_data(name)
            self.logger.info("Plugin \"%s\" destroyed." % (name))

    def get_plugin_name_list(self):
        return (self.pluginDict.keys())

    def get_plugin_object(self, name):
        return self.pluginDict[name][1]

    def _load_all_plugins(self):
        # preload all plugins
        sys.path.append(self.pluginDir)
        try:
            for fn in glob.glob(os.path.join(self.pluginDir, "*")):
                bn = os.path.basename(fn)
                exec("from %s import get_plugin_list" % (bn))
                exec("from %s import get_plugin_properties" % (bn))
                exec("from %s import get_plugin_object" % (bn))
                for name in eval("get_plugin_list()"):
                    self.pluginDict[name] = [eval("get_plugin_properties(name)"), eval("get_plugin_object")]
        finally:
            sys.path.remove(self.pluginDir)

        # filter plugin
        for name in self._get_sorted_plugin_names():
            for name2 in self.pluginDict[name][0].get("need-plugin", []):
                if name2 not in self.pluginDict:
                    self.logger.warn("Plugin %s is not loaded because dependent plugin %s does not exists." % (name, name2))
                    del self.pluginDict[name]
                    break

    def _init_all_plugins(self):
        for name in self._get_sorted_plugin_names():
            self.param.envObj.init_plugin_data(name)
            self.pluginDict[name][1] = self.pluginDict[name][1](name)
            self.pluginDict[name][1].init2(self.param.cfgObj, self.param.envObj)
            self.logger.info("Plugin \"%s\" initialized." % (name))

    def _get_sorted_plugin_names(self):
        tdict = dict()
        for name in self.pluginDict:
            tdict[name] = set(self.pluginDict[name][0].get("need-plugin", []))
        return toposort.toposort_flatten(tdict)
