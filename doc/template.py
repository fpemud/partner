#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-


class ReflexEnvironment:

    @property
    def is_user_login(self):
        # only exists in user scope
        assert False

    def set_plugin_data(self, plugin_name, data):
        assert False
    
    def get_plugin_data(self, plugin_name):
        # returns None if plugin_data is not set
        assert False

    def changed(self):
        # called by who modifies this object
        assert False
