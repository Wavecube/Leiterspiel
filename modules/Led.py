from MCP23S17 import MCP23S17
from modules.Component import Component


class Led(Component):

    def switch(self, state):
        self._chip.set_output_pin(self._sch, self._pin, state)

    def state(self):
        return self._chip.get_output_pin(self._sch, self._pin)
