#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
Blink randomly leds panels until keyboard interrupt.
"""

from automaton_client import AutomatonClient

SERVER_HOST = "localhost"
SERVER_PORT = 1502

try:
    c = AutomatonClient(host=SERVER_HOST, port=SERVER_PORT)

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (SERVER_HOST, SERVER_PORT))

    if c.is_open():
        # set panels on or off randomly
        while True:
            result = c.set_random()
            print("WROTE 23 regs")
    c.close()

except ValueError:
    print("Error with host or port params")

except (KeyboardInterrupt, SystemExit):
    # interrupting this script sets all panels to off
    c.clear_all()
    c.close()
