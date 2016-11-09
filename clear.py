from automaton_client import *

SERVER_HOST = "localhost"
SERVER_PORT = 1502

try:
    c = AutomatonClient(host=SERVER_HOST, port=SERVER_PORT)

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (SERVER_HOST, SERVER_PORT))

    if c.is_open():
        result = c.clear_all()
        if result:
            print("WROTE 23 regs from ad #12389")

    c.close()

except ValueError:
    print("Error with host or port params")
