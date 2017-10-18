#! /usr/bin/env python
# -*- coding:utf-8 -*-

import random
import time

from automaton_client import AutomatonClient
from utils.random import random6

SLEEP_INTERVAL = 5

# sets on only 6 randomly chosen panels



try:
    c = AutomatonClient()

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (c.host(), c.port()))

    if c.is_open():
        while True:
            result = c.write_all(random6())
            if result:
                print("WROTE 23 regs from ad #12389")
            time.sleep(SLEEP_INTERVAL)
    c.close()

except ValueError:
    print("Error with host or port params")

except (KeyboardInterrupt, SystemExit):
    # interrupting this script sets all panels to off
    c.clear_all()
    c.close()
