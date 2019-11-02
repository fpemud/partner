#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-


def get_plugin_list():
    # returns list<plugin-name>
    assert False


###############################################################################
# plugin-property-dict:
#     "need-plugin": list<plugin-name>
###############################################################################
def get_plugin_properties(name):
    # returns plugin-property-dict
    assert False


def get_plugin_object(name):
    # returns plugin-object
    assert False


class PluginObject:

    def init2(self, cfg, reflex_environment):
        assert False

    def dispose(self):
        assert False

    def get_good_reflexes(self, reflex_name, reflex_properties):
        # returns list<reflex-fullname>
        assert False

    def reflex_pre_init(self, reflex_fullname, reflex_properties, obj):
        assert False

    def reflex_post_fini(self, reflex_fullname, reflex_properties):
        assert False

