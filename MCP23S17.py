import spidev
import math

class MCP23S17:

    def __init__(self, slave_address, busnumber, chipnumber):
        # Das Programm abbrechen wenn der busnummer wert oder die chipnummer nicht zwischen 0 und 1 sind.
        assert busnumber in [0, 1]
        assert chipnumber in [0, 1]
        # fügt einen bit an das ende der adresse.
        self.controlbyte_write = slave_address<<1
        # fügt einen bit an das ende des Bytes und setzt diesen auf 1
        self.controlbyte_read = (slave_address<<1)+1
        # Stellt den SPI bus über die SpiDev library ein.
        self.spi = spidev.SpiDev()
        self.spi.open(busnumber, chipnumber)
        self.spi.max_speed_hz = 10000000
        # configure default registers
        self._regs = {'conf': {'A': 0x00, 'B': 0x01},
                      'input': {'A': 0x12, 'B': 0x13},
                      'output': {'A': 0x14, 'B': 0x15}}

    # schreibt in das Konfigurations register von einer der Ports.
    def write_config(self, portab, value):
        assert portab in ['A', 'B']
        reg = self._regs['conf'][portab]
        self.spi.xfer([self.controlbyte_write, reg, value])

    # liest das Kofigurationsregister von einer der Ports und gibt den gelesenen Wert zurück.
    def read_config(self, portab):
        assert portab in ['A', 'B']
        reg = self._regs['conf'][portab]
        return self.spi.xfer([self.controlbyte_read, reg, 0])[2]

    # Setzt den angegebenen Port auf die übergebenen Werte.
    def write_output(self, portab, value):
        assert portab in ['A', 'B']
        reg = self._regs['output'][portab]
        self.spi.xfer([self.controlbyte_write, reg, value])

    # ließt das Outputregister eines Ports und gibt es zrück.
    def read_output(self, portab):
        assert portab in ['A', 'B']
        reg = self._regs['output'][portab]
        return self.spi.xfer([self.controlbyte_read, reg, 0])[2]

    # ließt das Inputregister eines Ports und gibt es zrück.
    def read_input(self, portab):
        assert portab in ['A', 'B']
        reg = self._regs['input'][portab]
        return self.spi.xfer([self.controlbyte_read, reg, 0])[2]

    def set_output_pin(self, portab, pin, value):
        self.write_output(portab, self.__setPin(self.read_output(portab), pin, value))
    
    def get_output_pin(self, portab, pin):
        return self.__getPin(self.read_output(portab), pin)

    def get_input_pin(self, portab, pin):
        return self.__getPin(self.read_input(portab), pin)

    def __getPin(self, register, pin):
        y = 1<<pin
        return (register&y)>>pin
    
    def __setPin(self, register, pin, value):
        prev = self.__getPin(register, pin)
        rs = register
        if value:
            if not prev:
                rs = register|(1<<pin)
        else:
            if prev:
                rs = register&~(1<<pin)
        return rs
