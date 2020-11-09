from MCP23S17 import MCP23S17


class Component:
    def __init__(self, chip:MCP23S17, schnittstelle, pin):
        self._chip = chip
        self._sch = schnittstelle
        self._pin = pin