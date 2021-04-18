"""

RW  - GPIO13 (D7)
RS  - GPIO12 (D6)
E   - GPIO14 (D5)
PSB - GND

"""
from micropython import const
from time import sleep
from framebuf import FrameBuffer, MONO_HLSB

ST7920_DAT           = const(0xFA)    # Data
ST7920_CMD           = const(0xF8)    # Command

ST7920_CLEAR_SCREEN  = const(0x01)
ST7920_DISPLAY_CTRL  = const(0x0C)
ST7920_BASIC         = const(0x30)
ST7920_EXTEND        = const(0x34)

ST7920_WIDTH         = const(128)
ST7920_HEIGHT        = const(64)

class ST7920(FrameBuffer):    
    def __init__(self, spi, rst=None):
        self.spi = spi        
        self.rst = rst
        if rst:
            self.rst.init(self.rst.OUT, value=1)
        self.cmd = bytearray(3)
        self.buf = bytearray(ST7920_WIDTH * ST7920_HEIGHT // 8)
        super().__init__(self.buf, ST7920_WIDTH, ST7920_HEIGHT, MONO_HLSB)
        self.init()

    def _write(self, cmd, data):
        self.cmd[0] = cmd
        self.cmd[1] = (data & 0xF0)
        self.cmd[2] = ((data << 4) & 0xF0)
        self.spi.write(self.cmd)
    
    def init(self):
        if self.rst:
            self.rst(0)
            sleep(0.1)
            self.rst(1)
        for cmd in (ST7920_BASIC,
                    ST7920_CLEAR_SCREEN,
                    ST7920_DISPLAY_CTRL,
                    ST7920_EXTEND,
                    ST7920_EXTEND | 0x02):
            self._write(ST7920_CMD, cmd)
        self.show()
        
    
    def show(self):
        for i in range(0, len(self.buf), 2):
            x = (i // 2) % 8
            y = i // 16
            if i >= len(self.buf) // 2:
                x += 8
                y += 32
            self._write(ST7920_CMD, 0x80 | y)
            self._write(ST7920_CMD, 0x80 | x)
            self._write(ST7920_DAT, self.buf[i])
            self._write(ST7920_DAT, self.buf[i+1])
