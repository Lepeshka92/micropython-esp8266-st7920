from machine import SPI, Pin
from st7920 import ST7920

rst = Pin(5)
spi = SPI(1, baudrate=2000000)
lcd = ST7920(spi, rst)

lcd.text('Micropython', 2, 0)
lcd.text('Hello, world', 0, 1)