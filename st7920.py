"""

RW  - GPIO13 (D7)
E   - GPIO14 (D5)
PSB - GND

"""
from micropython import const
from time import sleep


ST7920_DAT           = const(0xFA)    # Data
ST7920_CMD           = const(0xF8)    # Command

ST7920_CLEAR_SCREEN  = const(0x01)    # Clear screen
ST7920_ENTRY_MODE    = const(0x06)    # Cursor direction to right
ST7920_DISPLAY_CTRL  = const(0x0C)    # Turns display on
ST7920_BASIC         = const(0x30)    # Basic instruction set

ST7920_WIDTH         = const(16)
ST7920_HEIGHT        = const(4)
ST7920_LINES         = (0x80, 0x90, 0x88, 0x98)

class ST7920:    
    def __init__(self, spi, rst=None):
        self.spi = spi
        self.rst = rst
        
        if self.rst:
            self.rst.init(self.rst.OUT, value=1)
        self.buf = bytearray(3)

        self.init()

    def _write(self, cmd, data):
        self.buf[0] = cmd
        self.buf[1] = (data & 0xF0)
        self.buf[2] = ((data << 4) & 0xF0)
        self.spi.write(self.buf)
    
    def reset(self):
        if self.rst:
            self.rst(0)
            sleep(0.1)
            self.rst(1)
    
    def init(self):
        self.reset()
        for cmd in (ST7920_BASIC,
                    ST7920_CLEAR_SCREEN,
                    ST7920_ENTRY_MODE,
                    ST7920_DISPLAY_CTRL):
            self._write(ST7920_CMD, cmd)
    
    def text(self, t, x, y):
        if y < 0 or y >= ST7920_HEIGHT:
            return
        if x < 0 or x >= ST7920_WIDTH:
            return

        addr = ST7920_LINES[y] + x // 2
        self._write(ST7920_CMD, addr)

        line = t[:ST7920_WIDTH-x]
        if x % 2 == 1:
            self._write(ST7920_DAT, 32)    #(((
        for c in line:
            self._write(ST7920_DAT, ord(c))