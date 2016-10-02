from pyModbusTCP.client import ModbusClient

SERVER_HOST = "localhost"
SERVER_PORT = 1502

try:
    c = ModbusClient(host=SERVER_HOST, port=SERVER_PORT)

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (SERVER_HOST, SERVER_PORT))

    # if open() is ok, read register (modbus function 0x03)
    if c.is_open():
        # read 10 registers at address 0, store result in regs list
        result = c.write_multiple_registers(12389, [0]*23)
        # if success display registers
        if result:
            print("WROTE 23 regs from ad #12389")

    c.close()

except ValueError:
    print("Error with host or port params")
