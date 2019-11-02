#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import dbus


class AssReflexEnvironment:

    def __init__(self, param):
        self.param = param

        if self.param.uid != 0:
            try:
                dbusObj = dbus.SystemBus().get_object("org.freedesktop.login1", "/org/freedesktop/login1")
                dbusObj.GetUser(self.param.uid, dbus_interface="org.freedesktop.login1.Manager")
                self.is_user_login = True
            except BaseException:
                self.is_user_login = False

        self.plugin_data_dict = dict()

    def init_plugin_data(self, plugin_name):
        self.plugin_data_dict[plugin_name] = None

    def set_plugin_data(self, plugin_name, data):
        assert self.plugin_data_dict[plugin_name] is None
        self.plugin_data_dict[plugin_name] = data

    def get_plugin_data(self, plugin_name):
        return self.plugin_data_dict[plugin_name]

    def remove_plugin_data(self, plugin_name):
        del self.plugin_data_dict[plugin_name]

    def changed(self):
        if self.param.reflexManager is not None:
            self.param.reflexManager.on_reflex_environment_changed()
