#! /usr/bin/env python
# -*- coding:utf-8 -*-

import random
import time

from automaton_client import AutomatonClient

SERVER_HOST = "localhost"
SERVER_PORT = 1502
SLEEP_INTERVAL = 5

# sets on only 6 randomly chosen panels
def random6():
    regs_values = [0] * 23
    indices = []
    while len(indices) < 6:
        val = random.randint(0, 22)
        print val
        if val not in indices:
            indices.append(val)
            regs_values[val] = 100
    return regs_values


try:
    c = AutomatonClient(host=SERVER_HOST, port=SERVER_PORT)

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (SERVER_HOST, SERVER_PORT))

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
