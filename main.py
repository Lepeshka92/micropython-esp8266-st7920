from machine import SPI, Pin
from st7920 import ST7920
from time import sleep

lcd = ST7920(SPI(1, baudrate=2000000), Pin(5))
lcd.text('Hello, world', 16, 30)
lcd.show()