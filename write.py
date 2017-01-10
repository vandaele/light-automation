#! /usr/bin/env python
# -*- coding:utf-8 -*-

import random

from automaton_client import AutomatonClient

SERVER_HOST = "localhost"
SERVER_PORT = 1502

# sets gradual values
regs_values = range(23)
regs_values = [item * 4 for item in regs_values]

# sets different panels lines values
regs_values = [80] * 4
regs_values += [5] * 4
regs_values += [5] * 4
regs_values += [80] * 4
regs_values += [20] * 5
regs_values += [65] * 2

# sets on only 6 randomly chosen panels
regs_values = [0] * 23
indices = []
while len(indices) < 6:
    val = random.randint(0, 22)
    print val
    if val not in indices:
        indices.append(val)
        regs_values[val] = 100


try:
    c = AutomatonClient(host=SERVER_HOST, port=SERVER_PORT)

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (SERVER_HOST, SERVER_PORT))

    if c.is_open():
        result = c.write_all(regs_values)
        if result:
            print("WROTE 23 regs from ad #12389")

    c.close()

except ValueError:
    print("Error with host or port params")
