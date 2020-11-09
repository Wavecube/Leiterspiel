from MCP23S17 import MCP23S17
from modules.Component import Component

class Taster(Component):

    def state(self):
        return self._chip.get_input_pin(self._sch, self._pin)