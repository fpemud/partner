#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-


def Context:

    @property
    def logger(self):
        assert False

    @property
    def tmpdir(self):
        assert False




dependency_has_custom_action(brain_node_id)

dependency_check(brain_node_id)

dependency_fulfill(brain_node_id)

# wait until stimulus is triggered
# returns None if reflex dependency is broken and the reflex process stops
# returns (brain-node-id, reponse-coro) if the stimulus is triggered and the reponse should be taken.
stimulus()

response()

parallel_response()





###############################################################################
# reflex-property-dict:
#     "need-plugin": list<plugin-name>
#     "need-user-login": true OR false
#     "knowledge": KNOWLEDGE
#     "hint-in": {
#         "hint-id": KNOWLEDGE,
#     }
#     "hint-out": {
#         "hint-id": KNOWLEDGE,
#     }
###############################################################################
def get_reflex_properties(name):
    # returns reflex-property-dict
    assert False







    @property
    def logger(self):
        assert False

    @property
    def tmpdir(self):
        assert False

    @property
    def my_name(self):
        # returns "reflex_name"
        assert False

    @property
    def my_instance_name(self):
        assert False

    @property
    def my_full_name(self):
        # returns (self.my_name + ":" + self.instance_name) if self.instance_name != ""
        # returns self.my_name if self.instance_name == ""
        assert False

    def on_init(self):
        assert False

    def on_fini(self):
        assert False


# additional content for user reflex
class ReflexObjectUser:

    @property
    def user_name(self):
        assert False

    def on_receive_hint(self, hint, parameters):
        assert False

    def send_hint(self, hint, parameters=None):
        assert False

