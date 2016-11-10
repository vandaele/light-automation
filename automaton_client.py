import random

from pyModbusTCP.client import ModbusClient

SERVER_HOST = "localhost"
SERVER_PORT = 1502

REGISTER_START = 12389
REGISTER_NB = 23


class AutomatonClient(ModbusClient):

    def read(self, index):
        return self.read_holding_registers(REGISTER_START+index)

    def read_all(self):
        return self.read_holding_registers(REGISTER_START, REGISTER_NB)

    def write(self, index, value):
        return self.write_single_register(REGISTER_START+index, value)

    def write_all(self, values):
        return self.write_multiple_registers(REGISTER_START, values)

    def clear(self, index):
        return self.write(index, 0)

    def clear_all(self):
        return self.write_all([0]*REGISTER_NB)

    def set_random(self):
        return self.write_all([random.randint(0, 1) * 100 for i in range(REGISTER_NB)])
