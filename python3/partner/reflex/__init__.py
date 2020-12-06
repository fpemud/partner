#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

# Copyright (c) 2005-2020 Fpemud <fpemud@sina.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import functools
import partner.brain


class StimulusError(Exception):

    def __init__(self, brain_node_id):
        assert isinstance(brain_node_id)
        self.brain_node_id = brain_node_id


class ResponseError(Exception):

    def __init__(self, brain_node_id):
        assert isinstance(brain_node_id)
        self.brain_node_id = brain_node_id


async def trigger_response(brain_node_id, response_coro):
    pass


async def notify(brain_node_id):
    pass


# decoration
def stimulus(func):
    func.__dict__["partner.reflex.stimulus"] = True
    return func


# decoration
def response(func):
    assert not func.__dict__.get("partner.reflex.parallel_response")
    func.__dict__["partner.reflex.response"] = True
    return func


# decoration
def parallel_response(func):
    assert not func.__dict__.get("partner.reflex.response")
    func.__dict__["partner.reflex.parallel_response"] = True
    return func
