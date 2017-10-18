#! /usr/bin/env python
# -*- coding:utf-8 -*-

from automaton_client import *

try:
    c = AutomatonClient()

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (c.host(), c.port()))

    if c.is_open():
        result = c.write_all([100]*23)
        if result:
            print("WROTE 23 regs from ad #12389")

    c.close()

except ValueError:
    print("Error with host or port params")
