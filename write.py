from pyModbusTCP.client import ModbusClient

SERVER_HOST = "localhost"
SERVER_PORT = 1502

regs_address = range(23)
regs_address = [item+12389 for item in regs_address]
regs_value = range(23)
regs_value = [item*4 for item in regs_value]

regs_value = [5]*4
regs_value += [80]*4
regs_value += [35]*4
regs_value += [50]*4
regs_value += [20]*5
regs_value += [65]*2

try:
    c = ModbusClient(host=SERVER_HOST, port=SERVER_PORT)

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to %s:%s" % (SERVER_HOST, SERVER_PORT))

    # if open() is ok, read register (modbus function 0x03)
    if c.is_open():
        # read 10 registers at address 0, store result in regs list
        result = c.write_multiple_registers(12389, regs_value)
        # if success display registers
        if result:
            print("WROTE 23 regs from ad #12389")

    c.close()

except ValueError:
    print("Error with host or port params")
