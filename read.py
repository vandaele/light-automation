#! /usr/bin/env python
# -*- coding:utf-8 -*-

from automaton_client import AutomatonClient


try:
    c = AutomatonClient()

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (c.host(), c.port()))

    # if open() is ok, read registers
    if c.is_open():
        regs = c.read_all()
        # if success display registers
        if regs:
            print("READ 23 regs from ad #12389: %s" % regs)

    c.close()

except ValueError:
    print("Error with host or port params")
