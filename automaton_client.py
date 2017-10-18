import random
import yaml

from pyModbusTCP.client import ModbusClient

with open("config.yml", 'r') as yamlfile:
    cfg = yaml.load(yamlfile)

REGISTER_START = cfg['REGISTER_START']
REGISTER_NB = cfg['REGISTER_NB']
SERVER_HOST = cfg['SERVER_HOST']
SERVER_PORT = cfg['SERVER_PORT']


class AutomatonClient(ModbusClient):
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT, *args, **kwargs):
        ModbusClient.__init__(self, host, port, *args,**kwargs)

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
